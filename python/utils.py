from os import listdir, unlink
from os.path import join, isfile, islink,isdir
from shutil import rmtree


def delete_folder_content(folder_path):

    for filename in listdir(folder_path):
        file_path = join(folder_path, filename)
        try:
            if isfile(file_path) or islink(file_path):
                unlink(file_path)
            elif isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print(f'No se pudo remover el archivo {filename}.')