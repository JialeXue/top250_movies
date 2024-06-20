import requests
from bs4 import BeautifulSoup
import json
import pprint

#download 10 pages of HTML
page_indexs= range(0, 250, 25)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def download_all_htmls():
    htmls = []
    for idx in page_indexs:
        url = f"https://movie.douban.com/top250?start={idx}&filter="
        print("craw html:", url)
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise Exception("error")
        htmls.append(r.text)
    return htmls

htmls = download_all_htmls()
htmls[0]

def parse_single_html(html):
    soup = BeautifulSoup(html, "html.parser")
    article_items = (
        soup.find("div", class_="article")
            .find("ol", class_="grid_view")
            .find_all("div", class_="item")
    )
    datas = []
    for article_item in article_items:
        rank = article_item.find("div", class_="pic").find("em").get_text()
        info = article_item.find("div", class_="info")
        title = info.find("span", class_="title").get_text()

        stars = (info.find("div", class_="bd")
                    .find("div", class_="star")
                    .find_all("span")
                 )

        rating_star = stars[0]["class"][0]
        rating_num = stars[1].get_text()
        comments = stars[3].get_text()

        datas.append({
            "rank": rank,
            "title": title,
            "rating_star": rating_star.replace("rating", "").replace("-t", ""),
            "rating_num": rating_num,
            "comments":comments.replace("人评价","")
        })
    return datas

pprint.pprint(parse_single_html(htmls[0]))

all_datas = []
for html in htmls:
    all_datas.extend(parse_single_html(html))
print(len(all_datas))