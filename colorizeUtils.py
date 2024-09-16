from PIL import Image, ImageEnhance
from deoldify import device
from deoldify.device_id import DeviceId
import torch
from deoldify.visualize import get_image_colorizer
import os


def tryUseGPU():
    device.set(device=DeviceId.GPU0)  # Set the device (GPU) for accelerated processing
    torch.backends.cudnn.benchmark = True  # Enable optimizations for GPU processing

    if not torch.cuda.is_available():  # Check if GPU is available
        print('GPU is not available. Switching to CPU.')


def enhance_contrast(image_path, factor=1.15):
    """
    Enhances the contrast of the image.
    
    :param image_path: Path to the input image
    :param factor: Contrast enhancement factor (1.0 means no change, >1.0 means increased contrast)
    :return: Path to the new image with enhanced contrast
    """
    with Image.open(image_path) as img:
        enhancer = ImageEnhance.Contrast(img)
        enhanced_image = enhancer.enhance(factor)
        
        enhanced_image_path = os.path.join("static_images", f"enhanced_{os.path.basename(image_path)}")
        enhanced_image.save(enhanced_image_path)
        return enhanced_image_path


def colorizeImage(image_path):
    """
    Colorizes the image.
    
    :param image_path: Path to the input image
    :return: Path to the new colorized image
    """
    colorizer = get_image_colorizer(artistic=True)
    
    # Enhance contrast before colorization
    enhanced_image_path = enhance_contrast(image_path)
    
    # Colorize the image with enhanced contrast
    colorized_image = colorizer.get_transformed_image(enhanced_image_path, render_factor=35)
    
    colorized_image_path = os.path.join("static_images", f"colorized_{os.path.basename(enhanced_image_path)}")
    colorized_image.save(colorized_image_path)
    
    # Remove the grayscale image after colorization
    if os.path.exists(enhanced_image_path):
        os.remove(enhanced_image_path)
    
    return colorized_image_path
