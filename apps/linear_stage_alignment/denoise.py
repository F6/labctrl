import matplotlib.pyplot as plt
import numpy as np
import sys
import cv2

from sklearn import decomposition
from skimage import img_as_float
import scipy.fftpack as fp
import pywt
import time


def denoise_GB(img_gray):
    # Gaussian Filter to reduce noise
    #   try increase the gaussian core size to filter more noise
    # img_gb = cv2.GaussianBlur(img_gray, (5, 5), 0)
    img_gb = cv2.GaussianBlur(img_gray, (51, 51), 0)
    return img_gb


def denoise_BF(img_gray):
    # If the image is too fucking noisy, apply the bilateral filter 
    # Apply bilateral filter with d = 15,  
    # sigmaColor = sigmaSpace = 75. 
    img_bf = cv2.bilateralFilter(img_gray, 15, 75, 75)
    # img_bf = cv2.bilateralFilter(img_gray, 101, 75, 75)
    return img_bf


def denoise_NlMeans(img_gray):
    # If the image is insanely noisy, apply the Non-local Means Denoising
    # increase first param (h) to increase denoise
    img_NlMeans = cv2.fastNlMeansDenoising(img_gray, None, 3.0, 7, 21)
    # img_NlMeans = cv2.fastNlMeansDenoising(img_gray, None, 50.0, 7, 21)
    return img_NlMeans


def denoise_PCA(img_gray):
    """Because when taking picture of scattered laser, the diffrection of
    laser causes a lot of particle-like noises in the image, it is desirable
    to remove the noise before further analysis
    """
    n_components = 16 # 256
    # estimator = decomposition.PCA(n_components=n_components, svd_solver='randomized', whiten=True)
    estimator = decomposition.PCA(n_components=n_components, svd_solver='full', whiten=True)
    print("Extracting the top %d PCs..." % (n_components))
    t0 = time.time()
    fit = estimator.fit_transform(img_gray)
    img_recons = estimator.inverse_transform(fit)
    # print("Components:", estimator.components_)
    # print("Eigenvalues:", estimator.explained_variance_)
    # print("Mean:", estimator.mean_)
    train_time = (time.time() - t0)
    print("done in %0.3fs" % train_time)
    img_recons = np.array(img_recons, dtype=np.uint8)
    return img_recons
