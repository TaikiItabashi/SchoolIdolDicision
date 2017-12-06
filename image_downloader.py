import urllib.request as req
import json, os

#print(json.dumps(idols, indent=4))

#カードの一覧を取得する
#取得できるリストは10件ずつとなっていて、リンク形式なので再帰的に関数を呼び出す
#取得した一覧はローカルファイルに出力
#二度目以降はファイルから読み出す
#戻り値：JSON(dic?)形式のカード一覧
card_lists = []
def get_card_lists():
    url = "http://schoolido.lu/api/cards/"          #API
    local_path = "SchoolIdolDicision/card_lists.json"    #ローカルファイルのパス
    if not os.path.exists(local_path):              #ローカルにファイルが存在しない場合
        print(url)
        res = req.urlopen(url)
        lists = json.load(res)
        if lists["next"] != None:                   #次のリストがあるとき
            next_link = lists["next"]
            for li in lists["results"]:
                card_lists.append(li)
            get_card_list(next_link)                #再帰
        else:                                       #次のリスト
            for li in lists["results"]:
                card_lists.append(li)
            f = open(local_path, 'w')
            json.dump(card_lists, f)
            return card_lists
    else:                                           #ローカルにファイルが存在する場合
        f = open(local_path, 'r')
        card_lists = json.load(f)
        return card_lists

#カードのサムネイル画像を取得する
def get_thumbnail(dir_path, keyword, search_type):
    if not os.path.exists(dir_path): os.mkdir(dir_path)
    card_lists = get_card_lists()
    result_lists = []
    if search_type == "name":
        for li in card_lists:       #キーワードで検索
            if li['idol']['name'] == keyword:
                result_lists.append(li)
        for li in result_lists:     #画像を保存
            #覚醒前
            if not li['round_card_image'] is None:
                image_url = "http:" + li['round_card_image']
                save_path = dir_path + str(li["id"]) + ".png"
                print(save_path)
                req.urlretrieve(image_url, save_path)
            #覚醒後
            if not li['round_card_idolized_image'] is None:
                image_url = "http:" + li['round_card_idolized_image']
                save_path = dir_path + str(li['id']) + "i.png"
                print(save_path)
                req.urlretrieve(image_url, save_path)

#main関数
name = [
    "Kousaka Honoka", "Sonoda Umi", "Minami Kotori",
    "Nishikino Maki", "Koizumi Hanayo", "Hosizora Rin",
    "Ayase Eli", "Toujou Nozomi", "Yazawa Niko"
]
for charname in name:
    path = "SchoolIdolDicision/image/" + charname + "/"
    get_thumbnail(path, charname, "name")
