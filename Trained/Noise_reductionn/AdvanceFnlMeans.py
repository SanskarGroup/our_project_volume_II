import cv2
from FastnlMeans import FastnlMeans
import matplotlib.pyplot as plt

def DenoisingImage(image_array, h=11, hForColorComponents=6, templateWindowSize=7, searchWindowSize=21):
    if image_array is None:
        print("Error: Invalid image data.")
        return
    
    # Apply Gaussian Blur to smoothen the noise before denoising
    blurred_image = cv2.GaussianBlur(image_array, (5, 5), 0)
    denoised_image = cv2.fastNlMeansDenoisingColored(
        blurred_image, None, h, hForColorComponents, templateWindowSize, searchWindowSize
    )
    
    row, col = 1, 3
    fig, axs = plt.subplots(row, col, figsize=(20, 10))
    fig.tight_layout()
    axs[0].imshow(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
    axs[0].set_title("Original Image with Noise")
    axs[1].imshow(cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB))
    axs[1].set_title("Gaussian Blurred Image")    
    axs[2].imshow(cv2.cvtColor(denoised_image, cv2.COLOR_BGR2RGB))
    axs[2].set_title("Denoised Image")
    plt.show()

image_path = 'Images/image9.HEIC'
image_object = FastnlMeans()
image_seg = image_object.denoise_image(image_path)
DenoisingImage(image_seg, h=15, hForColorComponents=10, templateWindowSize=7, searchWindowSize=21)