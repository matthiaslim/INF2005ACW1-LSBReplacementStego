import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def calculate_histogram(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    img_np = np.array(img)

    hist_r = cv2.calcHist([img_np], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([img_np], [1], None, [256], [0, 256])
    hist_b = cv2.calcHist([img_np], [2], None, [256], [0, 256])

    return hist_r, hist_g, hist_b


def normalize_histogram(hist):
    return hist / hist.sum()


def compare_images(image_path1, image_path2):
    # Validate input paths
    if not os.path.isfile(image_path1) or not os.path.isfile(image_path2):
        raise ValueError("One or both image paths are invalid.")

    # Calculate histograms
    hist1_r, hist1_g, hist1_b = calculate_histogram(image_path1)
    hist2_r, hist2_g, hist2_b = calculate_histogram(image_path2)

    # Normalize histograms
    hist1_r = normalize_histogram(hist1_r)
    hist1_g = normalize_histogram(hist1_g)
    hist1_b = normalize_histogram(hist1_b)

    hist2_r = normalize_histogram(hist2_r)
    hist2_g = normalize_histogram(hist2_g)
    hist2_b = normalize_histogram(hist2_b)

    return {
        'histogram1': (hist1_r, hist1_g, hist1_b),
        'histogram2': (hist2_r, hist2_g, hist2_b),
    }


# Example usage
# compare_images('quack.png', 'quack.png')
