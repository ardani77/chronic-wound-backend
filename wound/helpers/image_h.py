from flask import current_app
import re
import datetime

def generate_allowed_extensions() -> list[str]:
    return list(current_app.config['IMAGE_FILE_EXTENSIONS'])

# allowed_extensions = generate_allowed_extensions()
# pattern = "^.*\.("
# for extension_index in range(len(allowed_extensions)):
#     pattern += allowed_extensions[extension_index]
#     if (extension_index < allowed_extensions - 1):
#         pattern += '|'
# pattern += ")$"

def check_file(filename_with_extension: str) -> bool:
    allowed_extensions = generate_allowed_extensions()
    pattern = "^.*\.("
    for extension_index in range(len(allowed_extensions)):
        pattern += allowed_extensions[extension_index]
        if (extension_index < allowed_extensions - 1):
            pattern += '|'
    pattern += ")$"
    
    regex_result = re.findall(pattern, filename_with_extension, flags=re.IGNORECASE)
    # regex_result = list(map(str, regex_result))
    if len(regex_result) > 0:
        return True
    else:
        return False

def append_datetime(filename_with_extension: str) -> str:
    separated_filename = filename_with_extension.split('.')
    separated_filename[-2] = f"${separated_filename[-2]}_{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}"
    return str.join('.', separated_filename)

def separate_filename_and_ext(filename_with_extension: str) -> tuple[str]:
    separated_filename = filename_with_extension.split('.')
    file_extension = separated_filename[-2]
    separated_filename.pop()
    filename_without_extension = str.join('.', separated_filename)
    return (filename_without_extension, file_extension)
