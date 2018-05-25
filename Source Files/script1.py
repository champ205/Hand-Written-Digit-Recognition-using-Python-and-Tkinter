import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from resizeimage import resizeimage
from sklearn.svm import SVC
import pickle
from scipy import misc
from PIL import Image
import PIL
import imageio
from skimage import transform

if __name__ == "__main__":
    data = pd.read_csv('train.csv')

    features = data.iloc[:2000,1:]
    labels = data.iloc[:2000,0]

    for i in range(len(features)):
        digit = features.iloc[i]
        digit[digit<np.mean(digit)]=0
        digit[digit>=np.mean(digit)]=255
    for i in range(len(features)):
        digit = features.iloc[i]
        digit = digit.reshape((28,28))
        del_arr = []
        for j in range(28):
            if 255 not in digit[j]:
                del_arr.append(j)
        digit = np.delete(digit,del_arr,0)
        #removing columns
        del_arr = []
        digit = digit.T
        for k in range(28):
            if 255 not in digit[k]:
                del_arr.append(k)
        digit = np.delete(digit,del_arr,0)
        digit = digit.T
        misc.imsave('modified/'+str(i)+'.jpg',digit)
    for i in range(len(features)):
        img2 = Image.open('modified/'+str(i)+'.jpg')
        wpercent = (28/float(img2.size[0]))
        hsize = int((float(img2.size[1])*float(wpercent)))
        img3 = img2.resize((28,28),PIL.Image.ANTIALIAS)
        img3.save('modified/'+str(i)+'.jpg',img2.format)

    dataset_modified = pd.DataFrame(index=None,columns=None)

    for i in range(len(features)):
        img = imageio.imread('modified/'+str(i)+'.jpg')
        img = transform.resize(img,(28,28))
        img = img.astype(features.dtypes)
        img = misc.bytescale(img)
        img_test = []
        for eachRow in img:
            for eachPixel in eachRow:
                img_test.append(eachPixel)
        dataset_modified = dataset_modified.append(pd.Series(img_test),ignore_index=True)
    dataset_modified.insert(0,column='labels',value=labels)
    new_features = dataset_modified.iloc[:2000,1:]
    new_labels = dataset_modified.iloc[:2000,0]


    for i in range(len(new_features)):
        digit = new_features.iloc[i]
        digit[digit<np.mean(digit)]=0
        digit[digit>=np.mean(digit)]=255

    svm_clf1 = SVC(kernel='poly',degree=5,random_state=0)
    svm_clf1.fit(new_features,new_labels)

    pickle.dump(svm_clf1,open('final_model.sav','wb'))
    features.dtypes.to_csv('features_dtypes.csv')
