import re
import os

os.system('curl https://sakurazaka46.com/s/s46/search/artist -o members.html')
os.system('mkdir img')

with open('members.html',encoding='utf-8') as f:
    html_str = f.read()

pattern = re.compile(pattern=r'<li class="box" data-member=(.+?)</li>',flags=re.DOTALL)
tmp_m_list=re.findall(pattern=pattern,string=html_str)
member_dict={}
for m in tmp_m_list:
    member_id, member_url, img_url, name_kanji, name_kana,*_ = m.split('\n')
    member_id=member_id[-4:-2]
    member_url=member_url.split('"')[1].strip('?ima=0000')
    img_url=img_url.split('"')[1]
    name_kanji=name_kanji.split('>')[1].split('<')[0]
    name_kana=name_kana.split('>')[1].split('<')[0]
    newEntry = {member_id : {'member_url':member_url, 'img_url':img_url, 'name_kanji':name_kanji, 'name_kana':name_kana}}
    member_dict.update(newEntry)

for m in member_dict.items():
    img_url=re.sub(r'400_320_102400.jpg','1000_1000_102400.jpg',m[1]['img_url'])
    file_name=m[1]['name_kanji'].replace(' ','_')+'.jpg'
    os.system(f'curl https://sakurazaka46.com{img_url} -o img/{file_name}')