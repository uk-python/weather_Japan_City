import requests
from datetime import datetime, timedelta, timezone
import pandas as pd
import matplotlib.pyplot as plt
from config import API_KEY  # APIキーをconfig.pyからインポート

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Hiragino Sans', 'BIZ UDGothic', 'MS Gothic']


key = API_KEY  # config.pyからAPIキーを取得
city = input('都市名を入力してください: ')
if not city:
    city = 'Tokyo'

url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&lang=ja'

json_data = requests.get(url).json()
df = pd.DataFrame(columns=['気温'])
tz = timezone(timedelta(hours=+9), 'JST')

for dat in json_data['list']:
    jst = datetime.fromtimestamp(dat['dt'], tz)  # datetime型のまま
    temp = dat['main']['temp'] - 273.15  # ケルビン→摂氏
    df.loc[jst] = temp

# インデックスをDatetimeIndexに変換（念のため）
df.index = pd.to_datetime(df.index)

# 曜日を日本語で表示するためのリスト
weekdays = ['月', '火', '水', '木', '金', '土', '日']

# x軸ラベルを「月日(曜日)」形式に
labels = [''] * len(df.index)  # 空のラベルをデータの数だけ作成
used_weekdays = set()  # すでに使われた曜日を重複せずに記録する
for i, dt in enumerate(df.index):  # インデックスと日付を同時に取得
    wd = dt.weekday()  # 日付から曜日を調べる
    if wd not in used_weekdays:# まだその曜日が使われていなければ
        # 月/日(曜日)形式のラベルを作成
        labels[i] = f"{dt.month}/{dt.day}({weekdays[wd]})" #空のラベルに代入
        used_weekdays.add(wd)
    # すでにその曜日が使われていれば空文字のまま

df.plot(figsize=(15, 8))
plt.ylim(-10, 40)
plt.grid()
plt.xticks(df.index, labels, rotation=45)  # x軸ラベルを曜日付きに
plt.show()