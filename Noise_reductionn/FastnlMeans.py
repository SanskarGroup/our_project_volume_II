import cv2
import numpy as np
from matplotlib import pyplot as plt

class FastnlMeans:
    def __init__(self, h=11, hForColorComponents=6, templateWindowSize=7, searchWindowSize=21):
        self.h = h
        self.hForColorComponents = hForColorComponents
        self.templateWindowSize = templateWindowSize
        self.searchWindowSize = searchWindowSize

    def denoise_image(self, image_path):
    
        image_data = cv2.imread(image_path)
        if image_data is None:
            raise ValueError("Image not found or unable to read.")
        
        denoised_image = cv2.fastNlMeansDenoisingColored(
            image_data, None, self.h, self.hForColorComponents, self.templateWindowSize, self.searchWindowSize
        )
        
        return denoised_image

    def display_images(self, original_image, denoised_image):

        fig, axs = plt.subplots(1, 2, figsize=(15, 10))
        fig.tight_layout()
        axs[0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        axs[0].set_title("Noise Image")
        axs[1].imshow(cv2.cvtColor(denoised_image, cv2.COLOR_BGR2RGB))
        axs[1].set_title("Denoised Image")
        plt.show()
