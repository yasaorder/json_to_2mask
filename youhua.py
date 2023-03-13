import cv2
import numpy as np
from skimage.morphology import thin, skeletonize
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('datasets/json_png_01binary/01overpass_4.png', 0)

# 测试是否全为二值图
from skimage import io
image = io.imread('01overpass_1.png')
skel = skeletonize(image)
thinion = thin(img)

# 画子图对比
assert img is not None
f, ax = plt.subplots(2, 2)
ax[0,0].imshow(img)
ax[0,0].set_title('original')
ax[0,0].get_xaxis().set_visible(False)
ax[0,1].axis('off')
ax[1,0].imshow(thinion)
ax[1,0].set_title('morphology.thin')
ax[1,1].imshow(skel)
ax[1,1].set_title('morphology.skeletonize')
plt.show()

# cv2.imshow('overpass_1-.png', thinion)
# cv2.waitKey(0)
# cv2.destroyAllWindows()