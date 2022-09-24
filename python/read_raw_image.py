import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

original_image_path = 'original.JPG'

original_img = mpimg.imread(original_image_path)

# Datos de la imagen raw (output del DJI Thermal SDK)
raw_image_path = 'measure.raw'
width = 640
height = 512

with open(raw_image_path, 'rb') as f:
    data = f.read()
    #packed = np.fromfile(f, dtype='int16')
    packed = np.frombuffer(data, dtype='int16')

print("mínimo: " + str(min(packed)))
print("máximo: " + str(max(packed)))

reshaped = packed.reshape((height, width))
print(reshaped)

# Se crea una figura de 1x2
fig, axs = plt.subplots(nrows=1, ncols=2)

# Se agrega las imágenes a los subplot (tener en cuenta que se accede como array de 1D)
axs[0].imshow(original_img)
axs[1].imshow(reshaped, cmap='gray')

plt.show()
