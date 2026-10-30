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


SID = ['m1', 'm2', 'ma', 'mb', 'm3', 'mc']   # 科目の 切りかえの 名前（アドレスの 後ろ：https://math-terakoya.github.io/#m2 で 数学Ⅱ）


def card(key, subject, sid):
    g = G[key]
    return f'''      <div class="game">
        <img class="shot" src="img/{key}.jpg" alt="{e(g['title'])}の画面" width="360" height="640">
        <div class="body">
          <h3>{e(g['title'])}</h3>
          <div class="unit">{e(g['topic'])}</div>
          <div class="btns"><a class="btn" href="{key}/">▶ あそぶ</a><a class="btn sub" href="#qr-{key}">QR</a></div>
          <details><summary>くわしく</summary><p>{e(g['desc'])}</p><div class="chapters">{e(g['chapters'])}</div></details>
        </div>
      </div>'''


used, back = [], {}
subs = D['subjects']
n_all = sum(len(u['games']) for s in subs for u in s['units'])
tabs = lambda cur: '<nav class="tabs">' + ''.join(f'<a href="#{SID[i]}"' + (' class="on"' if i == cur else '') + f'>{e(s["name"])}</a>' for i, s in enumerate(subs)) + '</nav>'
out = ['<section class="win" id="games">', f'    <h2>▼ ゲーム（{n_all}本）</h2>', '    <p class="note tabnote">科目を えらんで ください。</p>', '    <div class="subjs">']
# さいしょに 出す 科目（いちばん はじめ）は 最後に 置く：ほかの 科目が 開いて いる ときは CSS（:target ~）で かくす
order = list(range(1, len(subs))) + [0]
for i in order:
    s = subs[i]
    out.append(f'    <section class="subj{" def" if i == 0 else ""}" id="{SID[i]}" data-name="{e(s["name"])}">')
    out.append('    ' + tabs(i))
    for u in s['units']:
        out.append(f'    <div class="unitname">{e(u["name"])}</div>')
        for key in u['games']:
            out.append(card(key, s['name'], SID[i]))
            used.append(key)
            back[key] = SID[i]
    out.append('    </section>')
out.append('    </div>')
out.append('  </section>')
used = [k for s in subs for u in s['units'] for k in u['games']]
missing = sorted(set(G) - set(used))
assert not missing, f'games.json の games に あるのに subjects に 入って いない：{missing}'
qrs = [f'<div class="qrbig" id="qr-{k}"><div class="code"><img src="qr/{k}.png" alt="{e(G[k]["title"])}のQRコード" width="280" height="280"></div>'
       f'<div class="name">{e(G[k]["title"])}</div><div class="url">{URL}{k}/</div><a class="btn" href="#{back[k]}">とじる</a></div>' for k in used]
t = open(os.path.join(HERE, 'index.template.html'), encoding='utf-8').read()
html = t.replace('<!-- GAMES -->', '\n'.join(out)).replace('<!-- QRS -->', '\n'.join(qrs))
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(html)
print('作った:', len(used), '本 ／', ' ・ '.join(f'{s["name"]}（' + '、'.join(u['name'] for u in s['units']) + '）' for s in D['subjects']))
