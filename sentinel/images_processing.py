import numpy as np
def cap_range(image, minimum=0, maximum=255):
    """
    adjusts all values to within a range
    """

    image = np.clip(image,0,255)
  
    return image

def exposure(image, expsure_val):
    """
    newValue = oldValue * (2 ^ exposureCompensation)

    exposure_val should be between 0 and 1
    """
    image = image * (2**expsure_val)


    new_image = cap_range(image)

    return new_image

