
import subprocess
from os.path import splitext, basename

DJI_THERMAL_SDK_LOCATION = 'dji_thermal_sdk/dji_irp.exe'


def process_image(image_source_path: str, save_path: str) -> int:
    '''
    Procesa la imagen térmica haciendo uso del DJI Thermal SDK.
    La imagen procesada es de tipo raw y mantiene en nombre de la imagen fuente pero con 
    la entensión .raw.

    Parameters
    ----------
    image_source_path : str
        Path de la imagen térmica
    save_path: str
        Path donde se guardará la imagen

    Returns
    -------
    int
        Código de retorno de la ejecución del SDK. Si es valor es 0 la ejecución fue exitosa.
        Caso contrario ocurrió un error al intentar usar el SDK con la imagen.
    '''

    # Se obtiene solo el nombre del archivo sin la extension
    # para nombrar el .raw con el mismo nombre que el archivo
    image_base_name = basename(image_source_path)
    file_name_without_extension = splitext(image_base_name)[0]

    # Se compone el comando a ejecutar
    cmd = f'{DJI_THERMAL_SDK_LOCATION} -s {image_source_path} -a measure -o {save_path}/{file_name_without_extension}.raw'

    # Se ejecuta el comando con un subproceso y se devuelve un código de error
    try:
        result = subprocess.run(cmd, capture_output=True)
        return_code = result.returncode
        return return_code
    # En caso haya error devolvemos valor de código de error
    except subprocess.CalledProcessError as error:
        return -1
