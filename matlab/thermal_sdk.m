%--------------------------------------------------------------------------
% Descripción: Script para hacer uso del thermal SDK
% Autor: Jorge Campos
%--------------------------------------------------------------------------

% Se define el nombre de la carpeta donde se colocan las térmicas
% originales
folderName = "termicas";

% Se valida que exista la carpeta "termicas", caso contrario se crea la
% carpeta y se da indicaciones al usuario
if not (isfolder(folderName))
    disp("No existe la carpeta"+ folderName+". Creando la carpeta...");
    mkdir(folderName);
    disp("Carpeta creada. Por favor, coloque las imágenes que desee procesar.");
    return;
end

% Seleccionamos todas las imágenes térmicas de la carpeta
imagenesTermicas = dir(folderName+"/*.jpg");

numeroImagenes = length(imagenesTermicas);

if numeroImagenes == 0
    disp("No se ha encontrado ninguna imágen para procesar.");
    return;
end
fprintf("Se ha encontrado %d imágenes para procesar.\n", numeroImagenes)

% Se hace uso del DJI Thermal SDK para procesar las imágenes térmicas
djiThermalSdkLocation = "dji_thermal_sdk/dji_irp_omp.exe";
comando = '"' + djiThermalSdkLocation + '" -s ' + folderName + ' -a measure -o measure_p';
dos(comando);


disp("FIN del programa!!");






