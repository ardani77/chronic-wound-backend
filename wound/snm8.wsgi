import logging
import sys
logging.basicConfig(stream=sys.stderr)
#sys.path.insert(0, '/home/username/ExampleFlask/')
from wound import create_app
application = create_app()