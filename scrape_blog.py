import re
import os
import json

os.system('mkdir wkdir')

# get member-id, member-blog-url, member-name
def get_member_list():
    if not os.path.exists('wkdir/bloglist.html'):
        os.system('curl https://sakurazaka46.com/s/s46/diary/blog/list -o wkdir/bloglist.html')

    pattern = re.compile(r'<li class="box member-([0-9]{2})">.+?<a href="(.+?)">.+?<p class="name">(.+?)</p>.+?</li>',flags=re.DOTALL)

    with open('wkdir/bloglist.html',encoding='utf-8') as f:
        html_str = f.read()

    result = pattern.findall(html_str)
    result_nl = []
    for entry in result:
        result_nl.append({'id':entry[0],'url':'https://sakurazaka46.com' + entry[1],'name':entry[2].lstrip().rstrip()})

    # print(result_nl)
    json.dump(result_nl,open('wkdir/member_list.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

# get blog-urls for each member
def get_blog_list():
    member_list=[{"id":"03",
    "url":"https://sakurazaka46.com/s/s46/diary/blog/list?ima=0000&ct=03",
    "name":"上村 莉菜"
    }]

    pattern = re.compile(r'\
                         <ul class="com-blog-part.+?">\
                         .+?\
                         <li class="box">\
                         .+?\
                         <a href="(.+?)">\
                         .+?\
                         <p class="date wf-a">\
                         (.+?)\
                        #  ([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})\
                         </p>\
                         .+?\
                         <h3 class="title">\
                         (.+?)\
                         </h3>\
                         .+?\
                         </ul>\
                         ',flags=re.DOTALL)

    for member in member_list:
        if not os.path.exists(f'wkdir/{member["id"]}.html'):
            os.system(f'curl "{member["url"]}" -o "wkdir/{member["id"]}.html"')

        with open(f'wkdir/{member["id"]}.html',encoding='utf-8') as f:
            html_str = f.read()

        
        result = pattern.findall('''<ul class="com-blog-part box3 fxpc"><li class="box"><a href="/s/s46/diary/detail/54514?ima=0000&cd=blog">
  <div class="wrap-bg">
    <p class="com-coverbox"><span class="img" style="background-image: url(/images/14/e01/5bb9f015672f20873bb60eface46e/1000_1000_102400.jpg);"></span></p>
    <div class="txt">
      <div class="prof fx">
        <div class="prof-in fx">
          <p class="ph">

<img src="/images/14/54a/291b5858cbffd4d131d5938a94fd7/400_320_102400.jpg" alt="">

          </p>
          <p class="name">上村 莉菜</p>
        </div>
      </div>
      <div class="date-title">
        <p class="date wf-a">2024/1/31</p>
        <h3 class="title">1月31日</h3>
      </div>
      <p class="lead">﻿




遅くなってしまいましたが、
2024年もよろしくお願いします！





今日から2日間、
ゆいぽんの卒業コンサートですね

初期の頃からずっと...</p>
    </div>
    <div class="btn-wrap">
      <p class="btn-type1s wf-a"><span>MORE</span></p>
    </div>
  </div>
</a></li></ul>''')
        # result = pattern.findall(html_str)
        result_nl = []
        for entry in result:
            result_nl.append({'url':entry[0],'date':entry[1],'title':entry[2]})

        json.dump(result_nl,open(f'wkdir/{member["id"]}_blog_list.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

if __name__ == '__main__':
    # patt=re.compile(r'[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}')
    # print(patt.findall('2024/1/1'))
    get_blog_list()