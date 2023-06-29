# coding = utf - 8
# 先确保有D:\pythonProject1\spider\doctor_img这个文件夹，或者在第86行代码修改图片保存位置，不然可能下载不了图片
# 因为有些文章是有视频的，这些文章里没有图片，所以在爬取的过程中会跳过

from bs4 import BeautifulSoup  # 网页解析，获取数据
import urllib.request  # 正则表达式
import urllib.error  # 指定URL，获取网页数据
import xlwt  # 进行excel操作
import json
import requests
import re


def main():
    baseurl = "https://www.soyoung.com/community/index?page=2"
    # 发送HTTP GET请求获取网页内容
    datalist, imgurl = getData(baseurl)
    # print(datalist)
    # print(len(datalist))
    savepath = "医美文章.xls"
    saveData(datalist, imgurl, savepath)


findurl = re.compile(r'<div class="blur-img" data-v-eb458b72=""><img alt="" data-v-eb458b72="" src="(.*?)"/>')


def getData(url):
    datalist = []
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 获取网页内容
        content = response.text
        # print(content)

        # 解析JSON数据
        data = json.loads(content)
        url = "https://www.soyoung.com/p"
        phtot_url = []

        try:
            singer = data["responseData"]
            k = singer["diary_data"]
            kk = k["list"]
            for i in range(0, len(kk)):
                data1 = []
                kkk = kk[i]
                # 获取data
                kkkn = kkk["data"]
                # 获取文章主要信息
                main_data = kkkn["base"]
                title = main_data["title"]
                data1.append(title)
                # phtot_name.append(title)
                number = main_data["post_id"]
                title_url = url + str(number)
                data1.append(title_url)
                phtot_url.append(title_url)
                summary = main_data["summary"]
                data1.append(summary)
                datalist.append(data1)

            return datalist, phtot_url
        except Exception as a:
            print('抱歉，没有获取到！')

    else:
        print('请求失败')


def saveData(datalist, imgurl, savepath):
    print(imgurl)
    # 获取图片
    num = 1
    for img_url in range(0,len(imgurl)):
        url = imgurl[img_url]
        photo_html = askURL(url)
        soup = BeautifulSoup(photo_html, "html.parser")
        for item in soup.find_all('div', class_="blur-img"):
            item = str(item)
            link = re.findall(findurl, item)

            for j in range(0, len(link)):
                a = link[j]
                img = requests.get(a)
                f = open(r"D:\pythonProject1\spider\doctor_img/%s.jpg" % num, 'wb')
                f.write(img.content)
                f.close()
                print("第%s张图片下载完毕" % num)
                num = num + 1

    print("save.....")
    # 创建xls文件
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建列表对象
    sheet = book.add_sheet('医美文章', cell_overwrite_ok=True)  # 创建工作表
    col = ("文章标题", "文章链接", "文章概要")
    for i in range(0, 3):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, len(datalist)):
        print("第%d条" % i)
        data = datalist[i]
        for j in range(0, 3):
            sheet.write(i + 1, j, data[j])  # 保存数据

    book.save(savepath)


def askURL(url):
    head = {  # 模拟浏览器头部信息，向服务器发送信息，伪装用的
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        #               "Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63 "
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48"
    }  # 用户代理，表示告诉服务器我们是什么类型的机器，本质上是告诉浏览器我们可以接收什么内容的信息

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        resp = urllib.request.urlopen(request)
        html = resp.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == '__main__':
    main()
