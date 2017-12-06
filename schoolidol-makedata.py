from sklearn import cross_validation
from PIL import Image
import os, glob
import numpy as np

#分類対象のカテゴリーを選ぶ
root_dir = "SchoolIdolDicision/Image"
categories = [
    "Kousaka Honoka", "Sonoda Umi", "Minami Kotori",
    "Nishikino Maki", "Koizumi Hanayo", "Hosizora Rin",
    "Ayase Eli", "Toujou Nozomi", "Yazawa Niko"
]
nb_classes = len(categories)
image_size = 50

#フォルダごとの画像データを読み込む
X = []  #画像データ
Y = []  #ラベルデータ
for idx, cat in enumerate(categories):
    image_dir = root_dir + "/" + cat
    files = glob.glob(image_dir + "/*.png")
    print("---", cat, "を処理中")
    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((image_size, image_size))
        data = np.asarray(img)
        X.append(data)
        Y.append(idx)
X = np.array(X)
Y = np.array(Y)

#学習データとテストデータを分ける
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save("SchoolIdolDicision/Image/SchoolIdol.npy", xy)
print("ok", len(Y))
