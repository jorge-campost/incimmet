
clear;
clc;
close all;

% Se lee el archivo
filename = 'measure.raw';
width = 640; height = 512;
fileId = fopen(filename,"r");
img = fread(fileId, height *  width, 'int16',0,'l');
fclose(fileId);

min_value = min(img);
max_value = max(img);
% Se reescala
img = reshape(img, [width, height]);


%img = img/10;
img = img';

% Se muestra el resultado
imshow(mat2gray(img));