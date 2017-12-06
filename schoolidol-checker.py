import schoolidol_keras as schoolidol
import sys, os
from PIL import Image
import numpy as np

#コマンドラインからファイル名を得る
if len(sys.argv) <= 1:
    print("schoolidol-checker.py (ファイル名)")
    quit()

image_size = 50
categories = [
    "高坂穂乃果", "園田海未", "南ことり",
    "西木野真姫", "小泉花陽", "星空凛",
    "絢瀬絵里", "東條希", "矢澤にこ"
]
birthday = ["8/3", "3/15", "9/12",
    "4/19","1/17","11/1",
    "10/21","6/9","7/22"
]

# 入力画像をNumpyに変換
X = []
files = []
for fname in sys.argv[1:]:
    img = Image.open(fname)
    img = img.convert("RGB")
    img = img.resize((image_size, image_size))
    in_data = np.asarray(img)
    X.append(in_data)
    files.append(fname)
X = np.array(X)

#CNNのモデルを構築
model = schoolidol.build_model(X.shape[1:])
model.load_weights("./Image/schoolidol-model.hdf5")

#データを予測
html = ""
pre = model.predict(X)
for i, p in enumerate(pre):
    y = p.argmax()
    print("+ 入力:", files[i])
    print("| 名前:", categories[y])
    print("| 誕生日:", birthday[y])
    html += """
        <h3>入力:{0}</h3>
        <div>
            <p><img src="{1}" width=300></p>
            <p>名前:{2}</p>
            <p>誕生日:{3}</p>
        </div>
    """.format(os.path.basename(files[i]),files[i], categories[y], birthday[y])

#レポートを保存
html = "<html><body style='text-align:center;'>" + "<style> p { margin:0;, padding:0; } </style>" + html + "</body></html>"

with open("./schoolidol-result.html", "w") as f:
    f.write(html)
