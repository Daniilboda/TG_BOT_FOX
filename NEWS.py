import json
import  requests
from bs4 import BeautifulSoup

def get_first_news():
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }
    url = 'https://www.foxnews.com/'
    req = requests.get(url=url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    all_articles = soup.find('div', id="wrapper", class_="wrapper").find(class_='page').find(class_='region-content-sidebar').find(class_='thumbs-2-7').find_all('h3', class_="title")

    all_news_dict = {}
    for news in all_articles:
        news = news.find('a')
        news_txt = news.text
        news_href = news.get('href')
        category = news_href.split('/')[3]
        all_news_dict[news_txt] = {'Category': category, 'Link': news_href}
    all_news_dict = dict(reversed(all_news_dict.items()))
    with open('news.json', 'w', encoding='utf-8') as file_w:
        json.dump(all_news_dict, file_w, indent=3, ensure_ascii=False)
    return 'Новости сохранены в файл!'


def check_updates():
    with open('news.json', 'r', encoding='utf-8') as file:
        news_dict = json.load(file)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }
    url = 'https://www.foxnews.com/'
    req = requests.get(url=url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    all_articles = soup.find('div', id="wrapper", class_="wrapper").find(class_='page').find(class_='region-content-sidebar').find(class_='thumbs-2-7').find_all('h3', class_="title")
    fresh_news = {}
    for news in all_articles:
        news = news.find('a')
        news_txt = news.text
        news_href = news.get('href')
        category = news_href.split('/')[3]
        if news_txt in news_dict:
            continue
        else:
            news_href = news.get('href')
            category = news_href.split('/')[3]
            news_dict[news_txt] = {'Category': category, 'Link': news_href}
            fresh_news[news_txt] = {'Category': category, 'Link': news_href}
    with open('news.json', 'w', encoding='utf-8') as file_w:
        json.dump(news_dict, file_w, indent=3, ensure_ascii=False)

        return fresh_news


def main():
    # print(get_first_news())
    check_updates()
if __name__ == "__main__":
    main()