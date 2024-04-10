import glob
import numpy as np
import matplotlib.pyplot as plt #グラフの作成などに用いる
import astropy.io.fits as fits  #「fits」と呼ばれる形式の画像の処理に用いる

########################
###  ###
#########################

def make_dark(obs_date):
    d_raw_dir = '../../obs/' + str(obs_date) +'/'
    darks = glob.glob(d_raw_dir+'dark*.fit')
    
    dark_images = np.empty((0, 3056, 3056))  

    for dark in darks:
        #print(dark)
        dark = fits.getdata(dark)
        dark_images = np.append(dark_images, dark[np.newaxis, :], axis=0) 

    #print(dark_images)
    head = fits.getheader(darks[0])
    exp = float(head['EXPTIME'])
    med_dark = np.median(dark_images/exp, axis=0)                              
    #print(med_dark)
    out_d = '../../calib/dark/' + str(obs_date)
    fits.writeto(out_d + '/dark.fit', med_dark, overwrite=True)  

def minus(raw_file, bm_file, dark):
    d = fits.getdata(dark)
    #d_header = fits.getheader(dark)
    #d_norm = d/float(d_header['EXPTIME'])

    f = fits.getdata(bm_file)
    f_header = fits.getheader(raw_file)
    
    dark_c = float(f_header['EXPTIME'])*d
    file_d = f - dark_c
    return file_d

"""
#ダーク画像を格納する箱を作る
dark_images = np.empty((0, 4112, 4096))  

#ダークの画像を重ねたリストを作り、中央値をとる

for d_file in d_files:
    print(d_file, d_files)
    dark = fits.getdata(d_file)
    dark_images = np.append(dark_images, dark[np.newaxis, :], axis=0) #箱にデータを入れる
    median = np.median(dark) #中央値
    stddev = np.std(dark) #標準偏差
    print(d_file, median, stddev)

#show(d_files)

#重ね合わせた重ね合わせたdark_imagesから中央値をとり出力

out_d = "../data/"+group+"/" + name + "/dark"                                     #ダーク画像の出力先ディレクトリ名
mkdir(out_d)                                                                #ディレクトリがないことを確認した後に作成してくれる関数
median_dark = np.median(dark_images, axis=0)                              #dark_images から中央値をとる
fits.writeto(out_d + '/dark' + ints + '.fit', median_dark, overwrite=True)  #作成したディレクトリにダーク画像を出力
dark = fits.getdata(out_d +'/dark'+ ints + '.fit')                        #作成したデータを取得

print(ints + "秒darkの積分が出来ました")
#print(dark)

#出力した画像を表示
#plot("dark", dark)

#いよいよダークを引く作業へ
print("解析前のデータを表示します")

#解析対象のデータを取得

for t_file in t_files:
  print(t_file, t_files)
  img = fits.getdata(t_file)
  before = img
  #plot("before", img)
  
before = img

out_ds = "../data/" + group + "/" + name + "/dark_sub" 
mkdir(out_ds)

out_ds_i = "../data/" + group + "/" + name + "/dark_sub/" + ints
mkdir(out_ds_i)

print(ints+"秒積分画像のダーク引き処理を実行中です...")
dark_sub_images = np.empty((0, 4112, 4096))

l=[]
for t_file in t_files:
    #対象画像からダークを差し引いて、ダーク引き完了
    print(t_file)
    filename = str(t_file).replace("../data/" + group+ "/" + name + "/", "")
    img = fits.getdata(t_file)
    #dark = np.flip(dark, axis=0)
    dark_sub = img - dark
    outputname = "../data/" + group + "/" + name  + "/dark_sub/" + ints + "/" + filename
    print(outputname)
    fits.writeto(outputname, dark_sub, overwrite=True)

    dimg = fits.getdata(outputname)
    median = np.median(dimg)
    stddev = np.std(dimg)
    l.append([img, dimg])
    #plt.show()

    dark_sub_images = np.append(dark_sub_images, dimg[np.newaxis, :], axis=0)
    median = np.median(dark_sub_images)
    stddev = np.std(dark_sub_images)

plot_two("raw", "darksub", l)
dark_sub_image = np.median(dark_sub_images)
#plot_one("darksub", dark_sub_images)

print("######################")
print("ダーク引きが終了しました！")
print("######################")
"""