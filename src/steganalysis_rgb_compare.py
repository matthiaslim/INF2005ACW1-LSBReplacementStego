import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
from PIL import Image

def calculate_p_value(chi_square_stat, df):
    p_value = 1 - chi2.cdf(chi_square_stat, df)
    return p_value

def calculate_histogram(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Convert image to RGB if it's not
    img = img.convert('RGB')
    
    # Convert to numpy array
    img_np = np.array(img)
    
    # Calculate histograms for each channel
    hist_r = cv2.calcHist([img_np], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([img_np], [1], None, [256], [0, 256])
    hist_b = cv2.calcHist([img_np], [2], None, [256], [0, 256])

    return hist_r, hist_g, hist_b

def normalize_histogram(hist):
    return hist / hist.sum()

# Apply Chi-Square method 
def compare_histograms(hist1, hist2, method=cv2.HISTCMP_CHISQR):
    return cv2.compareHist(hist1, hist2, method)

def plot_histograms(hist1, hist2, title1='Image 1', title2='Image 2'):
    fig, axes = plt.subplots(3, 2, figsize=(20, 10))
    fig.suptitle('Histogram Comparison')
    
    channels = ['Red', 'Green', 'Blue']
    for i in range(3):
        axes[i, 0].plot(hist1[i], color=channels[i].lower())
        axes[i, 0].set_title(f'{title1} - {channels[i]} Channel')
        
        axes[i, 1].plot(hist2[i], color=channels[i].lower())
        axes[i, 1].set_title(f'{title2} - {channels[i]} Channel')
    
    plt.show()

def compare_images(image_path1, image_path2):
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
    
    # Compare histograms
    comparison_r = compare_histograms(hist1_r, hist2_r)
    comparison_g = compare_histograms(hist1_g, hist2_g)
    comparison_b = compare_histograms(hist1_b, hist2_b)
    
    # Print comparison results
    print(f'Red Channel Comparison: {comparison_r}')
    print(f'Green Channel Comparison: {comparison_g}')
    print(f'Blue Channel Comparison: {comparison_b}')
    
    # Plot histograms
    plot_histograms([hist1_r, hist1_g, hist1_b], [hist2_r, hist2_g, hist2_b])

# Example usage
# compare_images('path_to_cover_image.jpg', 'path_to_stego_image.jpg')
compare_images('quack.png', 'quack_stg.png')