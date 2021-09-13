# coding:utf-8
import re
from bs4 import BeautifulSoup
import urllib.request
import ssl

output_path = "./sanguoyanyi/"

def DownloadContent(url):
    print(url)
    file = urllib.request.urlopen(url)
    data = BeautifulSoup(file, features="html.parser", from_encoding="utf8")
    title = data.title.string
    title = re.sub("_.*", "", title)

    section_text = data.select('pre[id="content"]')[0].text
    section_text = re.sub("read_adout\(\'read1'\);mobile_go\(\);", "\t", section_text)
    section_text = re.sub("read_adout\('read_middle'\);", "\t", section_text)
    section_text = "\t" + title + "\n\n" + section_text
    section_text = re.sub("\s+", "\r\n\t", section_text).strip("\r\n")

    with open(output_path + title + ".txt", "w") as f:
        f.write(url + '\n')
        f.write(section_text)

    next_str = '<a href="(.[^ ]*?)" title="三国演义[0-9]+">下一章</a>'
    next_url = re.compile(next_str).findall(str(data))[0]
    return next_url

if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    initurl = "https://www.xiaoshuodaquan.com/"
    url = "https://www.xiaoshuodaquan.com/sanguoyanyi/1"
    cnt = 0
    while True:
        url = DownloadContent(url)
        cnt += 1
        print("have finished %d\n" % cnt)
        if url == "b_7rx.htm":
            break
        else:
            url = initurl + url
