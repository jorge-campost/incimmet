import os
import matplotlib
import numpy as np
import glob
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize

from skimage.filters import threshold_multiotsu, thresholding, edges
from skimage.color import label2rgb
from skimage.measure import regionprops
from skimage.morphology import reconstruction

from thermal_sdk import process_image
from utils import delete_folder_content

TERMICAS_FOLDER = 'Térmicas'
LABELED_IMAGES_FOLDER = 'LabeledImg'
SEGMENTED_IMAGES_FOLDER = 'SegmentedImg'
RAW_IMAGES_FOLDER = 'raw'

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 512


def check_folders() -> bool:
    '''
    Se realiza una validación de las carpetas de trabajo necesarias para la ejecución del programa.
    Si no existen son creadas automáticamente. En caso existan, el contenido de estas es eliminado.
    Solo la carpeta térmicas envía un flag para terminar el programa ya que esta tiene existir porque
    debe contener las imágenes térmicas a procesar.
    '''
    # Verificación de la carpeta "Térmicas"
    exists = os.path.isdir(TERMICAS_FOLDER)
    if not exists:
        print(f'No existe la carpeta de trabajo {TERMICAS_FOLDER}.')
        print(f'Creando carpeta {TERMICAS_FOLDER}...')
        print('Agregue las imágenes térmicas en la carpeta e intente ejecutar el programa nuevamente.')
        os.mkdir(TERMICAS_FOLDER)
        # Se envía el flag para terminar el programa
        return False

    # Verificación de la carpeta "LabeledImg"
    exists = os.path.isdir(LABELED_IMAGES_FOLDER)
    if not exists:
        print(f'No existe la carpeta de trabajo {LABELED_IMAGES_FOLDER}.')
        print(f'Creando carpeta {LABELED_IMAGES_FOLDER}...')
        os.mkdir(LABELED_IMAGES_FOLDER)
    else:
        print(f'Eliminando contenido de la carpeta {LABELED_IMAGES_FOLDER}.')
        delete_folder_content(LABELED_IMAGES_FOLDER)

    # Verificación de la carpeta "SegmentedImg"
    # exists = os.path.isdir(SEGMENTED_IMAGES_FOLDER)
    # if not exists:
    #     print(f'No existe la carpeta de trabajo {SEGMENTED_IMAGES_FOLDER}.')
    #     print(f'Creando carpeta {SEGMENTED_IMAGES_FOLDER}...')
    #     os.mkdir(SEGMENTED_IMAGES_FOLDER)
    # else:
    #     print(f'Elimando contenido de la carpeta {SEGMENTED_IMAGES_FOLDER}.')
    #     delete_folder_content(SEGMENTED_IMAGES_FOLDER)

    exists = os.path.isdir(RAW_IMAGES_FOLDER)
    if not exists:
        print(f'No existe la carpeta de trabajo {RAW_IMAGES_FOLDER}.')
        print(f'Creando carpeta {RAW_IMAGES_FOLDER}...')
        os.mkdir(RAW_IMAGES_FOLDER)
    else:
        print(f'Eliminando contenido de la carpeta {RAW_IMAGES_FOLDER}.')
        delete_folder_content(RAW_IMAGES_FOLDER)

    return True


def main():

    # Se valida las carpetas de trabajo para la ejecución del programa
    if not check_folders():
        return

    # Se obtiene todos las imágenes '.jpg' de la carpeta
    images_list = glob.glob(TERMICAS_FOLDER+'/*.jpg')

    # Se valida que haya imágenes para procesar sino se termina el programa
    if not len(images_list) > 0:
        print("No hay imágenes para procesar.")
        return

    # Se crea un lista que contendrá la lista de imagénes procesadas correctamente
    processed_images_list = []

    print(f'Se procesarán {len(images_list)} imágenes.')

    # Se itera sobre cada imagen de la lista para ser procesado
    for image_path in images_list:
        print(f'- Procesando archivo: {image_path} -> ', end='')
        # Se valida que el archivo exista (solo por si acaso se borre el archivo en plena ejecución)
        is_file = os.path.isfile(image_path)
        if not is_file:
            continue
        else:
            result_code = process_image(image_path, RAW_IMAGES_FOLDER)
            if result_code == 0:
                print("OK")
                processed_images_list.append(image_path)
            else:
                print("No se puede procesar la imagen.")

    # Se valida la cantidad de imágenes que se pudieron procesar
    if not len(processed_images_list) > 0:
        print('No se pudo procesar ninguna imagen. Revisar las imágenes e intente nuevamente.')
        return
    print(f'Se procesaron {len(processed_images_list)} imágenes correctamente.')

    # Se itera sobre la lista de imagénes procesadas
    for image_path in processed_images_list:

        # Se obtiene el nombre base de la imagen
        image_base_name = os.path.basename(image_path)

        # Se obtiene el nombre del archivo sin la extensión
        image_base_name_without_extension = os.path.splitext(image_base_name)[
            0]
        # Se quita la parte final del nombre del archivo '_T'
        image_base_name_without_extension_without_prefix = image_base_name_without_extension.split('_T')[
            0]

        # Se lee el archivo .raw
        raw_image_path = f'{RAW_IMAGES_FOLDER}/{image_base_name_without_extension}.raw'

        # Se valida que exista el archivo .raw
        if not os.path.isfile(raw_image_path):
            continue
        
        # Abrimos el archivo .raw como bytes
        with open(raw_image_path, 'rb') as raw_image_file:
            image_bytes = raw_image_file.read()
            packed_bytes = np.frombuffer(image_bytes, dtype='int16')

        # Se ordena los bytes en un array según las dimensiones de la imagen térmica
        reshaped_image = packed_bytes.reshape(IMAGE_HEIGHT, IMAGE_WIDTH)

        # Se divide entre 10 para obtener los valores en °C
        processed_img = reshaped_image / 10

        # Se obtiene los máximos y mínimos de temperatura
        min_temperature_value = processed_img.min()
        max_temperature_value = processed_img.max()

        # Se suaviza la image para eliminar el ruido
        # Se utiliza un filtro gaussiano con sigma = 2.5 que tiene un efecto similar
        # a la implementación del imguidedfilter de Matlab
        processed_img = thresholding.gaussian(processed_img, sigma=2.5)

        # Se genera umbrales para la segmentación en regiones
        thresholds = threshold_multiotsu(processed_img, classes=4)

        # Se usa los valores umbrales para generar las regiones
        regions = np.digitize(processed_img, bins=thresholds)

        # Rellenamos los agujeros. Similar a L = imfill(L) de Matlab
        seed = np.copy(regions)
        seed[1:-1, 1:-1] = regions.max()
        mask = regions
        filled_regions = reconstruction(seed, mask, method='erosion').astype(int)

        # Se crea un esquema de color para las regiones etiquetadas
        # colors=['cyan', 'yellow', 'red']

        regions_colorized = label2rgb(
            filled_regions, colors=['cyan', 'yellow', 'red'], bg_label=0, bg_color='blue', kind='overlay')

        # Se guarda la imagen segmentada
        #mpimg.imsave(f'{SEGMENTED_IMAGES_FOLDER}/{image_base_name_without_extension_without_prefix}_S.jpg', regions_colorized)

        # Se crea un custom colormap para el ploteo
        # rojo (riesgo), amarillo (alerta), verde(estable)
        custom_cmap = matplotlib.colors.LinearSegmentedColormap.from_list('', ['red', 'yellow', 'green'])
        # custom_cmap = 'jet'

        # Plot de la figura térmica etiquetada
        dpi = 200
        px = 1/200  # pixel in inches
        fig = plt.figure(figsize=(1200*px, 700*px), dpi=dpi)
        plt.imshow(processed_img, cmap=custom_cmap)
        plt.axis('off')
        plt.title("Imagen térmica etiquetada")

        # Se añade las etiquetas con las temperaturas
        props = regionprops(filled_regions+1, processed_img)
        for p in props:
            intensity_mean = p.intensity_mean
            y, x = p.centroid
            plt.text(x, y, str(round(intensity_mean, 2))+'°C')

        # Se añade la barra de colores lateral
        m = cm.ScalarMappable(norm=Normalize(
            min_temperature_value, max_temperature_value), cmap=custom_cmap)
        plt.colorbar(m, location='left', label='Temperatura (°C)')

        # Se guarda la figura generada
        fig.savefig(
            f'{LABELED_IMAGES_FOLDER}/{image_base_name_without_extension_without_prefix}_L.jpg', format='jpg')

    print("Programa finalizado.")


if __name__ == "__main__":
    main()
