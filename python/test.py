from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
import pickle
def pickleLoad(pickleFile):
    pkl_file = open(pickleFile, 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data
data = pickleLoad('/Users/ryansaxe/Desktop/kaggle_parkinsons/accelerometry/LILY_dataframe')
data = data.reset_index(drop=True)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xs = data['x.mean']
ys = data['y.mean']
zs = data['z.mean']
ax.scatter(xs, ys, zs)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()