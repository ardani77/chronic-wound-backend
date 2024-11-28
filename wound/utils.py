from flask import current_app
import time, random, string
import locale
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.util import img_as_float
from skimage.filters import gaussian, sobel
from skimage.io import imread
from scipy.interpolate import RectBivariateSpline
import os.path as ospath

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def pad_timestamp(filename):
    name = filename.split('.')
    return name[0] + str(round(time.time())) + '.' + name[1]

def generate_passphrase(length):
    letters = string.ascii_letters
    return ''.join(random.choices(letters)[0] for i in range(length))

def number_to_currency(x):
    locale.setlocale( locale.LC_ALL, 'id_ID.UTF-8' )
    return locale.currency( x, grouping=True )

def automatic_annotation(path, cc, cr, rad):
    my_dpi = 96
    img = imread(path)
    im_gray = rgb2gray(img)
    im_gt = imread(path)

    # parameter set
    sigma=3.5
    sample=400
    alpha = 0.015
    beta = 10
    gamma = 0.001 # time step
    max_num_iter=500


    # snake init (circle)
    theta = np.linspace(0, 2*np.pi, sample)
    r = cr + rad*np.sin(theta)
    c = cc + rad*np.cos(theta)
    snake_init = np.array([r, c]).T

    snake_xy = snake_init[:, ::-1]
    x = snake_xy[:, 0].astype(float)
    y = snake_xy[:, 1].astype(float)
    n = len(x)



    # energy external
    ext = gaussian(im_gray, sigma)
    ext = img_as_float(ext)
    ext = ext.astype(float, copy=False)
    ext = sobel(ext)



    # energy internal

    a = beta
    b = -(4*beta + alpha)
    c = 6*beta + 2*alpha

    eye_n = np.eye(n, dtype=float)
    c_axis = c * eye_n
    b_axis = b * ( np.roll(eye_n, -1, axis=0) + np.roll(eye_n, -1, axis=1) )
    a_axis = a * ( np.roll(eye_n, -2, axis=0) + np.roll(eye_n, -2, axis=1) )
    A = c_axis + b_axis + a_axis

    # Only one inversion is needed for implicit spline energy minimization. skimage
    inv = np.linalg.inv(A + gamma * eye_n)
    inv = inv.astype(float, copy=False)


    # potential force
    gy, gx = np.gradient(ext)

    # Interpolate for smoothness
    intp1 = RectBivariateSpline(np.arange(gx.shape[1]),
                                np.arange(gx.shape[0]),
                                gx.T, kx=2, ky=2, s=0)

    intp2 = RectBivariateSpline(np.arange(gy.shape[1]),
                                np.arange(gy.shape[0]),
                                gy.T, kx=2, ky=2, s=0)


    # deform snake
    max_px_move=1.0

    #fig2= plt.figure(frameon=False, figsize=(img.shape[1]/my_dpi, img.shape[0]/my_dpi), dpi=my_dpi)
    #ax2 = fig2.add_axes([0, 0, 1, 1])
    #ax2.imshow(im_gray, cmap=plt.cm.gray)

    xt = np.copy(x)
    yt = np.copy(y)

    for i in range(max_num_iter):
            # fx & fy
            fx = intp1(xt, yt, dx=0, grid=False).astype(float, copy=False)
            fy = intp2(xt, yt, dy=0, grid=False).astype(float, copy=False)

            # skimage equation
            xn = np.dot(inv, gamma * xt + fx)
            yn = np.dot(inv, gamma * yt + fy)

            # Movements are capped to max_px_move per iteration. skimage
            dx = max_px_move * np.tanh(xn - xt)
            dy = max_px_move * np.tanh(yn - yt)

            xt += dx
            yt += dy

            # if i % 10 == 0:
            #         snake_iter = np.array([xt, yt]).T
            #         ax2.plot(snake_iter[:, 0], snake_iter[:, 1], '-g', lw=2)

    snake_final = np.array([xt, yt]).T
    #ax2.plot(snake_final[:, 0], snake_final[:, 1], '-b', lw=2)
    #ax2.set_xticks([]), ax2.set_yticks([]) # hide axes
    #ax2.axis('off')
    #outname2 = ospath.splitext(path)[0] + "_interp_result" + ospath.splitext(path)[1]
    #plt.savefig(outname2, dpi=my_dpi)
    #print(outname2 + " has been saved")
    ## plt.show()
    #plt.close(fig2)

    return snake_final.tolist()