import matplotlib.pyplot as plt
import numpy as np
import sys
import cv2

from sklearn import decomposition
from skimage import img_as_float
import scipy.fftpack as fp
import pywt
import time

from denoise import denoise_GB, denoise_PCA
from fit_gaussian_2D import getFWHM_GaussianFitScaledAmp


def limit_img_size(img, limitx=1080, limity=1440):
    imgx = img.shape[0]
    imgy = img.shape[1]
    print("Image has shape {} x {}, resizing to within {} x {}".format(
        imgx, imgy, limitx, limity))
    if imgx > limitx:
        imgy = limitx / imgx * imgy
        imgx = limitx
        print("Resized to {} x {} because x limit".format(imgx, imgy))
    if imgy > limity:
        imgx = limity / imgy * imgx
        imgy = limity
        print("Resized to {} x {} because y limit".format(imgx, imgy))
    imgx, imgy = int(imgx), int(imgy)
    print("Resized img to {} x {}".format(imgx, imgy))
    img_resized = cv2.resize(img, (imgy, imgx))
    return img_resized


def img_fullscale(img_gray):
    img = np.array(img_gray, dtype=np.uint8)
    imgmin = np.min(img)
    print("Minimum in image: {}, shifting minimum to 0".format(imgmin))
    img = img - imgmin
    imgmax = np.max(img)
    print("After shifting, maximum in image: {}, rescaling maximum to 255".format(imgmax))
    img_scale = img / imgmax * 255
    img_fs = np.array(img_scale, dtype=np.uint8)
    return img_fs


def my_show_img(img, code=cv2.COLOR_BGR2RGB, convert_to_uint=False):
    # cv_rgb = cv2.cvtColor(img, code)
    # fig, ax = plt.subplots(figsize=(16, 10))
    # ax.imshow(cv_rgb)
    # fig.show()
    if convert_to_uint:
        img = np.array(img, dtype=np.uint8)

    print("Limiting image size for showing")
    img_resized = limit_img_size(img)
    cv2.imshow("Preview", img_resized)
    cv2.waitKey(0)


def image_preprocess(img):
    """Preprocess the beam profile from a photo"""
    # First step, convert image to grayscale, limit it's size, then rescale to full scale for better numeric results
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("Limiting image size for processing")
    img_resized = limit_img_size(img_gray, 1024, 1024)
    img_fs = img_fullscale(img_resized)
    # Reducing noise with Gaussian Blur and PCA
    img_denoise = denoise_GB(img_fs)
    img_denoise = denoise_PCA(img_denoise)
    img_denoise_fs = img_fullscale(img_denoise)
    # Fit denoised image with 2D Gaussian
    # img_fit = limit_img_size(img_gray, 128, 128)
    print("Fitting single Gaussian beam profile...")
    x, y, dx, dy, amp, offset = getFWHM_GaussianFitScaledAmp(img_denoise_fs)
    # x = x*4
    # y = y*4
    # dx=dx*4
    # dy=dy*4
    print("Fitted single Gaussian beam, x={}, y={}, FWHM(x)={}, FWHM(y)={}, Amplitude={}, Offset={}".format(
        x, y, dx, dy, amp, offset))
    center_coordinates = (int(x), int(y))
    axesLength = (int(dx/2), int(dy/2))
    angle = 0
    startAngle = 0
    endAngle = 360
    color = (255, 255, 255)
    thickness = 2
    # ======== Redraw image with pseudocolor for better contract ========
    img_denoise_fs = cv2.applyColorMap(img_denoise_fs, cv2.COLORMAP_JET)
    img_denoise_fs = cv2.ellipse(img_denoise_fs, center_coordinates, axesLength,
                                 angle, startAngle, endAngle, color, thickness)
    img_fs = cv2.applyColorMap(img_fs, cv2.COLORMAP_JET)
    img_fs = cv2.ellipse(img_fs, center_coordinates, axesLength,
                         angle, startAngle, endAngle, color, thickness)
    axesLength = (int(dx), int(dy))
    img_denoise_fs = cv2.ellipse(img_denoise_fs, center_coordinates, axesLength,
                                 angle, startAngle, endAngle, color, thickness)
    img_fs = cv2.ellipse(img_fs, center_coordinates, axesLength,
                         angle, startAngle, endAngle, color, thickness)
    start_point = (int(x), 0)
    end_point = (int(x), img_denoise_fs.shape[0])
    img_denoise_fs = cv2.line(img_denoise_fs, start_point, end_point, color, thickness)
    img_fs = cv2.line(img_fs, start_point, end_point, color, thickness)
    start_point = (0, int(y))
    end_point = (img_denoise_fs.shape[1], int(y))
    img_denoise_fs = cv2.line(img_denoise_fs, start_point, end_point, color, thickness)
    img_fs = cv2.line(img_fs, start_point, end_point, color, thickness)
    return img_denoise_fs, img_fs


img = cv2.imread("examples/0002.jpg")
print("Img Size: ", img.shape)
img_denoise_fs, img_fs = image_preprocess(img)

img_show = np.concatenate((img_fs, img_denoise_fs), axis=1)
my_show_img(img_show)