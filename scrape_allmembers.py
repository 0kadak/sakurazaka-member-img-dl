
import re
import os

print(f'Scraping website for image urls')
os.system('curl https://sakurazaka46.com/s/s46/page/formation -so formation.html')
os.system('mkdir img')

with open('formation.html',encoding='utf-8') as f:
    html_str = f.read()

pattern=re.compile(r'<li>(<a href="/s/s46/artist/\d+\?ima=0000">)?<span style="background-image: url\(\'(.+?)\'\);"></span><i>(.+?)</i>(</a>)?</li>')
result = pattern.findall(html_str)
r=[(x[1],x[2]) for x in result]
sortedlist=sorted(set(r),key=lambda x:x[1])

members={}
for el in sortedlist:
    img_url=el[0].replace('200_320','1000_1000')
    if ' ' in el[1]: name=el[1].replace(' ','')
    else: name=el[1]

    if name not in members:
        members[name]=[img_url]
    else: members[name].append(img_url)

for m in members.items():
    count=0
    print(f'Downloading {len(m[1])} images for {m[0]}')
    for url in m[1]:
        os.system(f'curl https://sakurazaka46.com{url} -so img/{m[0]}_{count}.jpg')
        count+=1