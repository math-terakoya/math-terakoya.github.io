"""寺子屋の 入口の ページ（index.html）を、games.json と index.template.html から 作る。
科目・単元・並び順・ゲームの 説明は games.json を 直す。使い方: python3 build.py
"""
import json
import os
from html import escape as e

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'games.json'), encoding='utf-8'))
G = D['games']
URL = 'https://math-terakoya.github.io/'


def card(key, subject):
    g = G[key]
    return f'''      <div class="game win">
        <img class="shot" src="img/{key}.jpg" alt="{e(g['title'])}の画面" width="360" height="640">
        <div>
          <h3>{e(g['title'])}</h3>
          <div class="unit">{e(subject)} ／ {e(g['topic'])}</div>
          <p>{e(g['desc'])}</p>
          <div class="chapters">{e(g['chapters'])}</div>
          <div class="btns"><a class="btn" href="{key}/">▶ あそぶ</a><a class="btn sub" href="#qr-{key}">QR を 大きく 表示</a></div>
        </div>
      </div>'''


used = []
out = ['<section class="win" id="games">', f'    <h2>▼ ゲーム（{sum(len(u["games"]) for s in D["subjects"] for u in s["units"])}本）</h2>']
for s in D['subjects']:
    out.append(f'    <h2 class="subject">{e(s["name"])}</h2>')
    for u in s['units']:
        out.append(f'    <div class="unitname">{e(u["name"])}</div>')
        for key in u['games']:
            out.append(card(key, s['name']))
            used.append(key)
out.append('  </section>')
missing = sorted(set(G) - set(used))
assert not missing, f'games.json の games に あるのに subjects に 入って いない：{missing}'
qrs = [f'<div class="qrbig" id="qr-{k}"><div class="code"><img src="qr/{k}.png" alt="{e(G[k]["title"])}のQRコード" width="280" height="280"></div>'
       f'<div class="name">{e(G[k]["title"])}</div><div class="url">{URL}{k}/</div><a class="btn" href="#games">とじる</a></div>' for k in used]
t = open(os.path.join(HERE, 'index.template.html'), encoding='utf-8').read()
html = t.replace('<!-- GAMES -->', '\n'.join(out)).replace('<!-- QRS -->', '\n'.join(qrs))
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(html)
print('作った:', len(used), '本 ／', ' ・ '.join(f'{s["name"]}（' + '、'.join(u['name'] for u in s['units']) + '）' for s in D['subjects']))
