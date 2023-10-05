import glob
import os

def output():
    print('get dark file')

#ディレクトリの有無を確認し、ない場合は作る関数
def mkdir(out):
  if os.path.exists(out)==False:
      os.mkdir(out)

#ほしい天体のデータを持ってくる
def get_date_obj(dir, date, obj):
   files = glob.glob(str(dir) + "/" + str(date) + "/" + str(obj) + "*.fit")
   print(files)
   return files