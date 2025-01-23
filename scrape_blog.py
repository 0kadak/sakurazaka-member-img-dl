import re
import os
import json

os.system('mkdir wkdir')

# get member-id, member-blog-url, member-name and save it to member_list.json
def get_member_list():
    if not os.path.exists('wkdir/bloglist.html'):
        os.system('curl https://sakurazaka46.com/s/s46/diary/blog/list -o wkdir/bloglist.html')

    pattern = re.compile(r'<li\s+class="box member-([0-9]{2})">.+?<a\s+href="(.+?)">.+?<p\s+class="name">(.+?)</p>.+?</li>',flags=re.DOTALL)

    with open('wkdir/bloglist.html',encoding='utf-8') as f:
        html_str = f.read()

    result = pattern.findall(html_str)
    result_nl = []
    for entry in result:
        result_nl.append({'id':entry[0],'url':'https://sakurazaka46.com' + entry[1],'name':entry[2].lstrip().rstrip()})

    json.dump(result_nl,open('wkdir/member_list.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

# get maxpage for each member and save it to member_list.json
def get_maxpage():
    with open('wkdir/member_list.json',encoding='utf-8') as f:
        member_list = json.load(f)
    
    for member in member_list:
        if not os.path.exists(f'wkdir/{member["id"]}.html'):
            os.system(f'curl "{member["url"]}" -o "wkdir/{member["id"]}.html')

        with open(f'wkdir/{member["id"]}.html',encoding='utf-8') as f:
            html_str = f.read()
        pattern = re.compile(r'<li><a href="/s/s46/diary/blog/list\?ima=0000&page=([0-9]+)&ct=[0-9]{2}&cd=blog">→</a></li>\s*</ul>',flags=re.DOTALL)
        result = pattern.findall(html_str)
        assert len(result) > 0, f'something wrong with regex pattern, too many matches: {result}'
        member["maxpage"]=int(result[0])
    json.dump(member_list,open('wkdir/member_list.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

# get blog-urls for each member
def get_blog_list():
    with open('wkdir/member_list.json',encoding='utf-8') as f:
        member_list = json.load(f)
    
    for member in member_list:
        with open(f'wkdir/{member["id"]}_blog_list.json','w',encoding='utf-8') as f: pass
        pattern = re.compile(rf'<li\s+class="box">.*?<a\s+href="(.+?)">.*?<p\s+class="name">{member["name"]}</p>.*?<p\s+class="date\s+wf-a">(.+?)</p>.*?<h3\s+class="title">(.*?)</h3>.*?</a>.*?</li>',flags=re.DOTALL)
        result_nl = []
        for i in range(member["maxpage"]+1):
            maxbar=10
            progress = int(maxbar*(i+1)/(member["maxpage"]+1))
            print(f'processing {member["name"]}\tpage{i}...\t[{"#"*progress}{" "*(maxbar-progress)}]',end='\r')
            if os.path.getsize(f'wkdir/{member["id"]}_blog_list.json') > 0:
              with open(f'wkdir/{member["id"]}_blog_list.json',encoding='utf-8') as f:
                  result_nl=json.load(f)
            if not os.path.exists(f'wkdir/{member["id"]}_{i}.html'):
                os.system(f'curl "{member["url"]}&page={i}" -o "wkdir/{member["id"]}_{i}.html"')

            with open(f'wkdir/{member["id"]}_{i}.html',encoding='utf-8') as f:
                html_str = f.read()
            result = pattern.findall(html_str)
            for entry in result:
                result_nl.append({'url':entry[0],'date':entry[1],'title':entry[2]})
        print()
        json.dump(result_nl,open(f'wkdir/{member["id"]}_blog_list.json','a',encoding='utf-8'),ensure_ascii=False,indent=2)

def get_stat():
    files=[f for f in os.listdir('wkdir') if os.path.isfile(os.path.join('wkdir',f)) and f.endswith('blog_list.json')]
    print(files)
    for f in files:
        with open(f'wkdir/{f}',encoding='utf-8') as j:
            data=json.load(j)
        print(f'{f} has {len(data)} entries')

def get_img():
    with open('wkdir/member_list.json',encoding='utf-8') as f:
        member_list = json.load(f)
    member_list = member_list[:1] # to specify which member to download
    for member in member_list:
        if os.name=='nt': os.system(f'mkdir img\{member["id"]}')
        else: os.system(f'mkdir img/{member["id"]}')

        with open(f'wkdir/{member["id"]}_blog_list.json',encoding='utf-8') as f:
            blog_list = json.load(f)
        for i, blog in enumerate(blog_list):
            maxbar=20
            progress = int(maxbar*(i+1)/(len(blog_list)))
            print(f'Img DL [{"#"*progress}{" "*(maxbar-progress)}] {member["name"]}-{blog["title"]}\t\t\t',end='\r')

            blog_id = blog["url"].split('/')[-1].split('?')[0]
            if not os.path.exists(f'wkdir/{member["id"]}_{blog_id}.html'):
                os.system(f'curl "https://sakurazaka46.com{blog["url"]}" -o "wkdir/{member["id"]}_{blog_id}.html')
            with open(f'wkdir/{member["id"]}_{blog_id}.html',encoding='utf-8') as f:
                html_str = f.read()
            pattern = re.compile(r'<img\s+src="(.+?)".+?>')
            result = pattern.findall(html_str)
            for i,img in enumerate(result):
                filename= img.split('/')[-1].split('.')[0]
                if filename.startswith('icon'): continue
                elif filename.startswith('jasrac'): continue
                elif filename.startswith('sakurazaka46'): continue
                os.system(f'curl -s "https://sakurazaka46.com{img}" -o "img/{member["id"]}/{blog_id}_{filename}.jpg"')
    print('done.')


if __name__ == '__main__':
    # get_member_list()
    # get_maxpage()
    # get_blog_list()
    # get_stat()
    get_img()