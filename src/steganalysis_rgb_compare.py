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


def plot_histograms(hist1, hist2, title1='Cover Image', title2='Stego Image'):
    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    fig.suptitle('Histogram Comparison')

    channels = ['Red', 'Green', 'Blue']
    for i, channel in enumerate(channels):
        axes[i, 0].plot(hist1[i], color=channel.lower())
        axes[i, 0].set_title(f'{title1} - {channel} Channel')

        axes[i, 1].plot(hist2[i], color=channel.lower())
        axes[i, 1].set_title(f'{title2} - {channel} Channel')

        # Plot differences
        diff = hist1[i] - hist2[i]
        axes[i, 2].plot(diff, color=channel.lower())
        axes[i, 2].set_title(f'Difference - {channel} Channel')

    plt.show()


def compare_images(image_path1, image_path2):
    print(image_path1)
    print(image_path2)
    hist1_r, hist1_g, hist1_b = calculate_histogram(image_path1)
    hist2_r, hist2_g, hist2_b = calculate_histogram(image_path2)

    hist1_r = normalize_histogram(hist1_r)
    hist1_g = normalize_histogram(hist1_g)
    hist1_b = normalize_histogram(hist1_b)

    hist2_r = normalize_histogram(hist2_r)
    hist2_g = normalize_histogram(hist2_g)
    hist2_b = normalize_histogram(hist2_b)

    # Plot histograms and their differences
    plot_histograms([hist1_r, hist1_g, hist1_b], [hist2_r, hist2_g, hist2_b])
    print("Reached")

# Example usage
#compare_images('quack.png', 'quack.png')
