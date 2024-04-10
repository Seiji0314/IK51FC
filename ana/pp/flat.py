import glob
import numpy as np
import astropy.io.fits as fits  #「fits」と呼ばれる形式の画像の処理に用いる

def make_flat(obs_date):
    f_raw_dir = '../../obs/' + str(obs_date) +'/'
    out_dir_dark = '../../calib/dark/' + str(obs_date)
    out_dir_flat = '../../calib/flat/' + str(obs_date)

    flats = glob.glob(f_raw_dir+'flat*.fit')
    bands = ['U', 'B', 'V', 'R', 'I', 'L']

    flat_images = np.empty((0, 3056, 3056))  

    for band in bands:
        flat_images = np.empty((0, 3056, 3056))  
        flats_band = [fl for fl in flats if band in fl]

        for flat_band in flats_band:
            flat = fits.getdata(flat_band)
            flat_images = np.append(flat_images, flat[np.newaxis, :], axis=0) 

        #print(flat_images)
        head = fits.getheader(flats_band[0])
        exp = float(head['EXPTIME'])
        med_flat = np.median(flat_images/exp, axis=0)                              
        #print(med_dark)

        med_dark = fits.getdata(out_dir_dark +'/dark.fit')
        med_flat = med_flat - med_dark

        fits.writeto(out_dir_flat + '/flat_'+band+'.fit', med_flat, overwrite=True) 

def norm(raw_file, dm_file, flat):
    #d = fits.getdata(dark)
    #d_head = fits.getheader(dark)
    #d_norm = d/float(d_head['EXPTIME'])

    fl = fits.getdata(flat)
    print(fl)
    #fl_head = fits.getheader(flat)
    #fl_norm = fl/float(fl_head['EXPTIME'])

    fi = fits.getdata(dm_file)

    fl_head = fits.getheader(raw_file)
    file_fn = fi/fl
    return file_fn