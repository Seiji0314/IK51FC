import numpy as np
import astropy.io.fits as fits
from astropy import stats
import glob
import matplotlib.pyplot as plt
from astropy.stats import sigma_clipped_stats
from photutils import DAOStarFinder
from photutils import aperture_photometry
from photutils import CircularAperture, CircularAnnulus


def locst(file):
    img = fits.getdata(file)
    mean, median, std = sigma_clipped_stats(img, sigma=3.0)

    daofind = DAOStarFinder(fwhm=3.0, threshold=5.0*std)  
    sources = daofind(img)  
    print(sources)

    positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
    apertures = CircularAperture(positions, r=9.)
    plt.figure(figsize=(14, 14))
    plt.imshow(img, plt.cm.gray, vmin=median - 5*std, vmax = median + 5*std, origin='lower', interpolation='none')
    apertures.plot(color='blue', lw=2.0, alpha=1.0)

    #各星の周りの局所的な背景を測定する。各星を中心とした輪っかを作成。
    annulus_apertures = CircularAnnulus(positions, r_in=10., r_out=15.)
    
    # どうなってるか見てみましょう
    plt.figure(figsize=(14, 14))
    plt.imshow(img, plt.cm.gray, vmin=median - 5*std, vmax=median + 5*std, origin='lower', interpolation='none')
    apertures.plot(color='blue', lw=3)
    annulus_apertures.plot(color='red', lw=3)
    #plt.xlim(550, 750)
    #plt.ylim(100, 300)
    #plt.xlim(400, 600)
    #plt.ylim(400, 600)