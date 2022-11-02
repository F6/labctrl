# Compute FWHM(x,y) using 2D Gaussian fit, min-square optimization
# Optimization fits 2D gaussian: center, sigmas, baseline and amplitude
# works best if there is only one blob and it is close to the image center.
# author: Nikita Vladimirov @nvladimus (2018).
# based on code example: https://stackoverflow.com/questions/21566379/fitting-a-2d-gaussian-function-using-scipy-optimize-curve-fit-valueerror-and-m

# Modified x@zzi.io 20221102 for py3 compatibility

import numpy as np
import scipy.optimize as opt


def twoD_GaussianScaledAmp(xdata_tuple, xo, yo, sigma_x, sigma_y, amplitude, offset):
    """Function to fit, returns 2D gaussian function as 1D array"""
    (x, y) = xdata_tuple
    xo = float(xo)
    yo = float(yo)
    g = offset + amplitude * \
        np.exp(- (((x-xo)**2)/(2*sigma_x**2) + ((y-yo)**2)/(2*sigma_y**2)))
    return g.ravel()


def getFWHM_GaussianFitScaledAmp(img):
    """Get FWHM(x,y) of a blob by 2D gaussian fitting
    Parameter:
        img - image as numpy array
    Returns: 
        centers, FWHMs in pixels, along x and y axes.
    """
    x = np.linspace(0, img.shape[1], img.shape[1])
    y = np.linspace(0, img.shape[0], img.shape[0])
    x, y = np.meshgrid(x, y)
    # Parameters: xpos, ypos, sigmaX, sigmaY, amp, offset
    initial_guess = (img.shape[1]/2, img.shape[0]/2, 100, 100, 1, 0)
    opt_bounds = ((img.shape[1]*0.1, img.shape[0]*0.1, 30, 30, 0.1, -0.1),
                  (img.shape[1]*0.9, img.shape[0]*0.9, img.shape[1]/2, img.shape[0]/2, 1.9, 0.5))
    # subtract background and rescale image into [0,1], with floor clipping
    bg = np.percentile(img, 5)
    img_scaled = np.clip((img - bg) / (img.max() - bg), 0, 1)
    popt, pcov = opt.curve_fit(twoD_GaussianScaledAmp,
                               (x, y),
                               img_scaled.ravel(),
                               p0=initial_guess,
                               bounds=opt_bounds)
    xcenter, ycenter, sigmaX, sigmaY, amp, offset = popt[
        0], popt[1], popt[2], popt[3], popt[4], popt[5]
    FWHM_x = np.abs(4*sigmaX*np.sqrt(-0.5*np.log(0.5)))
    FWHM_y = np.abs(4*sigmaY*np.sqrt(-0.5*np.log(0.5)))
    return (xcenter, ycenter, FWHM_x, FWHM_y, amp, offset)
