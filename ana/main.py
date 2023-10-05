import pp
import glob                     #ファイルの検索、ファイル名の取得などに用いる
import sys, os                  #pythonスクリプト上でコマンドを動かす
import subprocess
import astropy.io.fits as fits  #「fits」と呼ばれる形式の画像の処理に用いる

pp.gf_output()
pp.pi_output()

#dir = input('観測データのディレクトリを教えてください: ')
dir = '/Users/seiji/Desktop/astro/30_astr/obs'
date = input('観測日時を教えてください（例-20230820） : ')
name = input('天体の名前を教えて下さい（英数字）: ')

calib_make = input('較正用データを更新しますか？ （y or n）: ')
if calib_make == 'y':
  print('較正用データを更新します')
  calib_date = input('新しい較正用データの観測日時を教えてください（最新-20230902） : ')
bands = ['_B', '_V', '_R', '_I']
#rawc = input('生データのコピーを行いますか？[y/n] : ')

###############
### set dir ###
###############
dir_rd = '/Users/seiji/Desktop/astro/30_astr/res/'+date
dir_rdo = dir_rd + '/' + name 
dir_rdob = dir_rdo + '/bm'
dir_rdod = dir_rdo + '/dm'
dir_rdof = dir_rdo + '/fn'
dir_rdos = dir_rdo + '/sm'

dirs = [dir_rd, dir_rdo, dir_rdob, dir_rdod, dir_rdof, dir_rdos]

for di in dirs:
    pp.gf_mkdir(di)

##################
### make calib ###
##################
if calib_make == 'y':
  ### BIAS ###
  pp.b_make(calib_date)

  ### DARK ###
  pp.d_make(calib_date)

  ### FLAT ###
  pp.f_make(calib_date)

  ### SKYs ###
  #pp.f_make(calib_date)

################
### get file ###
################

### TARGET ###
files = pp.gf_do(dir, date, name)
#for file in files:
#  pp.pi_plot(name,file)

### BIAS ###
biases = pp.gf_do('/Users/seiji/Desktop/astro/30_astr/calib/bias', '20230902', 'bias')
#darks = pp.gf_do(dir, '20230825', 'dark_60')
#for dark in darks:

### DARK ###
darks = pp.gf_do('/Users/seiji/Desktop/astro/30_astr/calib/dark', '20230902', 'dark')
#darks = pp.gf_do(dir, '20230825', 'dark_60')
#for dark in darks:

### FLAT ###
flats = pp.gf_do('/Users/seiji/Desktop/astro/30_astr/calib/flat', '20230902', 'flat')
#for flat in flats:
#  pp.pi_plot(name,flat)

### SKY ###
#skys = pp.gf_do(dir, '20230825', 'flat_10_ -002')
#for flat in flats:
#  pp.pi_plot(name,flat)

print(files, biases, darks, flats)

##################
### minus bias ###
##################

for band in bands:
    file = [f for f in files if band in f][0]
    bias = biases[0]
    print(file, bias)
    file_bm = pp.b_minus(bias, file)
    #pp.pi_show(band, file_dm)
    fits.writeto(dir_rdob + '/' + name + band +'.fit', file_bm, overwrite=True)  #作成したディレクトリにダーク画像を出力

##################
### minus dark ###
##################

bms = glob.glob(dir_rdob + '/*')
print(bms)

for band in bands:
    file = [f for f in files if band in f][0]
    bm = [f for f in bms if band in f][0]
    dark = darks[0]
    #print(files, bm, dark)
    file_dm = pp.d_minus(file, bm, dark)
    #pp.pi_show(band, file_dm)
    fits.writeto(dir_rdod + '/' + name + band +'.fit', file_dm, overwrite=True)  #作成したディレクトリにダーク画像を出力

##################
### flat norm. ###
##################

dms = glob.glob(dir_rdod + '/*')
print(dms)

for band in bands:
    file = [f for f in files if band in f][0]
    file_dm = [fd for fd in dms if band in fd][0]
    flat = [fl for fl in flats if band in fl][0]
    dark = darks[0]
    print(file, file_dm, flat)
    file_dm_fn = pp.f_norm(file, file_dm, flat)
    pp.pi_show(band, file_dm_fn)
    fits.writeto(dir_rdof + '/fn' + band +'.fit', file_dm_fn, overwrite=True)  #作成したディレクトリにダーク画像を出力

#################
### minus sky ###
#################

for band in bands:
    pass

#print(date +"の"+ name +"　"+ints+"秒の積分画像を一次処理を行うためにディレクトリを整理します（生データのコピー："+rawc+"）...")

#go = input("入力に誤りはありませんか？ [y/n] : ")