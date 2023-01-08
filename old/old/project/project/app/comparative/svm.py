from getEmbeddings import getEmbeddings
print("8")
import numpy as np
print("8")
from sklearn.svm import SVC
print("8")
import matplotlib.pyplot as plt
print("8")
import scikitplot.plotters as skplt
print("8")

def plot_cmat(yte, ypred):
    '''Plotting confusion matrix'''
    skplt.plot_confusion_matrix(yte,ypred)
    plt.show()


xtr,xte,ytr,yte = getEmbeddings("datasets/train.csv")
print("1")
np.save('./xtr', xtr)
np.save('./xte', xte)
np.save('./ytr', ytr)
np.save('./yte', yte)

xtr = np.load('./xtr.npy')
xte = np.load('./xte.npy')
ytr = np.load('./ytr.npy')
yte = np.load('./yte.npy')
print("2")
clf = SVC()
clf.fit(xtr, ytr)
y_pred = clf.predict(xte)
m = yte.shape[0]
n = (yte != y_pred).sum()
print("Accuracy = " + format((m-n)/m*100, '.2f') + "%")   # 88.42%

#plot_cmat(yte, y_pred)
import pickle
filename = 'svmmodel.sav'
pickle.dump(clf, open(filename, 'wb'))

