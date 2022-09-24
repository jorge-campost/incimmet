data = load("RedEnrenada_SegSeman.mat"); 
net = data.net;

I = imread('W.JPG');
I = imresize(I, [720,960]);
cmap = ThermalColorMap();
C = semanticseg(I, net);

B = labeloverlay(I,C,'Colormap',cmap,'Transparency',0.4);
imshow(B);

function cmap = ThermalColorMap()
% Define el colormap utilizado en la imagenes etiquetadas.

cmap = [
    000 000 170 % "Zona de menor temperatura"
    000 000 255 % "Zona Intermedia 1"
    000 085 255 % "Zona Intermedia 2"
    000 170 255 % "Zona Intermedia 3"
    000 255 255 % "Zona Intermedia 4"
    085 255 170 % "Zona Intermedia 5"
    170 255 085 % "Zona Intermedia 6"
    255 255 000 % "Zona Intermedia 7"
    255 170 000 % "Zona Intermedia 8"
    255 085 000 % "Zona de mayor temperatura"
    ];
cmap = cmap ./ 255;
end