import numpy as np
import glob 
import matplotlib.pyplot as plt #グラフの作成などに用いる
import astropy.io.fits as fits  #「fits」と呼ばれる形式の画像の処理に用いる

def make_bias(obs_date):
    b_raw_dir = '/Users/seiji/Desktop/astro/30_astr/obs/' + str(obs_date) +'/'
    biases = glob.glob(b_raw_dir+'bias*.fit')

    bias_images = np.empty((0, 3056, 3056))  

    for bias in biases:
        #print(bias)
        bias = fits.getdata(bias)
        bias_images = np.append(bias_images, bias[np.newaxis, :], axis=0) 

    #print(bias_images)
    med_bias = np.median(bias_images, axis=0)                              
    #print(med_bias)
    
    out_d = '/Users/seiji/Desktop/astro/30_astr/calib/bias/' + str(obs_date)
    fits.writeto(out_d + '/bias.fit', med_bias, overwrite=True)  

def minus(bias, file):
    b = fits.getdata(bias)
    #b_header = fits.getheader(bias)
    #b_norm = b/float(b_header['EXPTIME'])

    f = fits.getdata(file)
    f_header = fits.getheader(file)
    
    bias = b
    file_b = f - bias
    return file_b