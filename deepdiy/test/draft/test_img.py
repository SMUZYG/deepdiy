from scipy import misc
f = misc.face()
misc.imsave('face.jpg', f) # uses the Image module (PIL)

import matplotlib.pyplot as plt
plt.imshow(f)
plt.show()
