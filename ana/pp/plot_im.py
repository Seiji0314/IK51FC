import numpy as np
import matplotlib.pyplot as plt #グラフの作成などに用いる
import astropy.io.fits as fits  #「fits」と呼ばれる形式の画像の処理に用いる

def output():
    print('plot image')

# function for plot to copare two images
def plot(name, data):
  #出力した画像を表示
  img = fits.getdata(data)
  median = np.median(img)
  stddev = np.std(img)
  print(median, stddev)
  plt.figure(figsize=(7, 7))
  plt.imshow(img, plt.cm.gray, vmin=median - stddev, vmax = median + stddev, origin='lower', interpolation='none')
  plt.title(name)
  plt.show()
  plt.close()

def show(name, data):
  #出力した画像を表示
  img = data
  median = np.median(img)
  stddev = np.std(img)
  print(median, stddev)
  plt.figure(figsize=(7, 7))
  plt.imshow(img, plt.cm.gray, vmin=median - stddev, vmax = median + stddev, origin='lower', interpolation='none')
  plt.title(name)
  plt.show()
  plt.close()

# function for plot to copare two images
def plot_one(name1, ndarray):
  image = np.median(ndarray, axis=0)
  median = np.median(image)
  stddev = np.std(image)
  plt.figure(figsize=(8, 8))
  plt.title(name1)
  plt.imshow(image, plt.cm.gray, vmin=median - stddev, vmax = median + stddev, origin='lower', interpolation='none')
  plt.show()
  plt.close()

# function for plot to copare two images
def plot_two(name1, name2, ndarray):
  fig, axes = plt.subplots(1, 2, figsize=(20,10))
  title1 = name1
  title2 = name2 
  axes[0].set_title(title1)
  axes[1].set_title(title2)

  for i in range(1):
    for j in range(2):
      med = np.median(ndarray[i][j])
      std = np.std(ndarray[i][j])
      #axes[i][j].title()
      axes[j].imshow(ndarray[i][j], plt.cm.gray, vmin=med - std, vmax = med + std, origin='lower', interpolation='none')

  plt.close()