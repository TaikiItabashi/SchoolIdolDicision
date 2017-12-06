from PIL import Image
import os, glob
import numpy as np
import random, math

#分類対象
root_dir = "SchoolIdolDicision/Image"
categories = [
    "Kousaka Honoka", "Sonoda Umi", "Minami Kotori",
    "Nishikino Maki", "Koizumi Hanayo", "Hoshizora Rin",
    "Ayase Eli", "Toujou Nozomi", "Yazawa Nico"
]
nb_classes = len(categories)
image_size = 50

#画像データを読み込む
#フォルダごとの画像データを読み込む
X = []  #画像データ
Y = []  #ラベルデータ
def add_sample(cat, fname, is_train):
    img = Image.open(fname)
    img = img.convert("RGB")
    img = img.resize((image_size, image_size))
    data = np.asarray(img)
    X.append(data)
    Y.append(cat)
    if not is_train: return

    #角度を変えたデータを追加
    for ang in range(-20, 20, 5):
        img2 = img.rotate(ang)
        data = np.asarray(img2)
        X.append(data)
        Y.append(cat)

        #反転
        img2 = img2.transpose(Image.FLIP_LEFT_RIGHT)
        data = np.asarray(img2)
        X.append(data)
        Y.append(cat)

def make_sample(files, is_train):
    global X, Y
    X = []
    Y = []
    for cat, fname in files:
        add_sample(cat, fname, is_train)
    return np.array(X), np.array(Y)

#ディレクトリごとにわけられたファイルを収集
allfiles = []
for idx, cat in enumerate(categories):
    image_dir = root_dir + "/" + cat
    files = glob.glob(image_dir + "/*.png")
    for f in files:
        allfiles.append((idx, f))

#シャッフルして学習データとテストデータに分ける
random.shuffle(allfiles)
th = math.floor(len(allfiles) * 0.6)
train = allfiles[0:th]
test = allfiles[th:]
X_train, y_train = make_sample(train, True)
X_test, y_test = make_sample(test, False)
xy = (X_train, X_test, y_train, y_test)
np.save("SchoolIdolDicision/Image/schoolidol2.npy", xy)
print("ok", len(y_train))


X = np.array(X)
Y = np.array(Y)
