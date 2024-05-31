import requests
from bs4 import BeautifulSoup
from newspaper import Article
import csv

# URL cua trang chu VnExpress
BASE_URL = "https://vnexpress.net/"


# Gui yeu cau HTTP va lay noi dung HTML
def fetch_page(url):
    respone = requests.get(url)
    respone.raise_for_status()  # Kiem tra loi HTTP
    return respone.text


# Phan tich HTML va lay cac lien ket bai viet
def get_article_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for link in soup.find_all("a", href=True):
        url = link["href"]
        if "vnexpress.net" in url and url not in links:
            links.append(url)
    return links


# Lay thong tin chi tiet tu bai viet
def get_article_details(url):
    article = Article(url)
    article.download()
    article.parse()
    return {
        "url": url,
        "title": article.title,
        "author": ", ".join(article.authors),
        "publish_date": article.publish_date,
        "content": article.text,
    }


# Luu thong tin vao file csv
def save_to_csv(
    data, filename="E:/Project/VnExpress_WebCrawler/vnexpress_articles.csv" # Thay doi duong dan file khi clone source code ve may
):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


# Main
def main():
    # Lay noi dung tu trang chu
    homepage_html = fetch_page(BASE_URL)
    # Thu thap cac lien ket tu trang chu
    article_links = get_article_links(homepage_html)
    articles_data = []

    for link in article_links:
        try:
            # Lay thong tin chi tiet tu cac bai viet
            article_details = get_article_details(link)
            articles_data.append(article_details)
            # Dung lai khi da thu thap du 1000 bai viet
            if len(articles_data) >= 1000:
                break
        except Exception as e:
            print(f"Error fetching article {link}: {e}")

    # Luu vao file csv
    save_to_csv(articles_data)


if __name__ == "__main__":
    main()
