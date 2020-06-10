import platform


system = platform.system()

def dir_separater():
    if system == 'Windows':
        return '\\'
    return '/'
