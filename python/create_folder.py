import os


IMAGES_FOLDER = 'INCIMMET'
documents_path = os.path.join(
    os.path.expanduser('~'), 'Documents', IMAGES_FOLDER)

exists = os.path.isdir(documents_path)
if not exists:
    print("No existe la carpeta")
    os.mkdir(documents_path)
else:
    print("Sí existe")
