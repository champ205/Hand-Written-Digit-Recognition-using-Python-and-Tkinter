import pickle
import imageio
from skimage import transform
from scipy import misc
from PIL import Image
import numpy as np
import PIL
import pandas as pd

features_dtype = pd.Series.from_csv('features_dtypes.csv')
classifier_model = pickle.load(open('final_model.sav','rb'))

img = imageio.imread('out_snapsave.jpg')
img = transform.resize(img, (28,28))
img = img.astype(features_dtype)
img = misc.bytescale(img)
x_test = []
for eachRow in img:
    for eachPixel in eachRow:
        x_test.append(sum(eachPixel)/3)
x_test = np.array(x_test)
#Binarization
x_test[x_test<225]=0
x_test[x_test>=225]=255
#Removing rows
x_test = x_test.reshape((28,28))
del_arr=[]
for i in range(len(x_test)):
    if 255 not in x_test[i]:
        del_arr.append(i)
x_test = np.delete(x_test,del_arr,0)
#Removing Columns
x_test=x_test.T
del_arr=[]
for i in range(len(x_test)):
    if 255 not in x_test[i]:
        del_arr.append(i)
x_test = np.delete(x_test,del_arr,0)
x_test = x_test.T
misc.imsave('error.jpg',x_test)
img2 = Image.open('error.jpg')
wpercent = (28/float(img2.size[0]))
hsize = int((float(img2.size[1])*float(wpercent)))
img3 = img2.resize((28,28),PIL.Image.ANTIALIAS)
img3.save('error3.jpg',img2.format)

img = imageio.imread('error3.jpg')
img = transform.resize(img,(28,28))
img = img.astype(features_dtype)
img = misc.bytescale(img)
img_test = []
for eachRow in img:
    for eachPixel in eachRow:
        img_test.append(eachPixel)
img_test = np.array(img_test)
img_test = img_test.reshape([1,784])
img_test[img_test<np.mean(img_test)]=0
img_test[img_test>=np.mean(img_test)]=255
file = open("output.txt","w+")
file.write(str(int(classifier_model.predict(img_test)[0])))
file.close()
