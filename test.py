import asyncio
import aiohttp
from bs4 import BeautifulSoup
import datetime
import time


start_time = time.time()
result = []
cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

cookies = {
    'csrftoken':
        '38LU3tgTgto1PsaoIKjCNTDftxri2Pxrnb0AbnemmOKcA0Xp7pxg7h4dchdntUAg',
    'sessionid': '9tp28dt3d0j77m4wsf2tmijzpkcye9us',
    'is_authenticated': '1',
    'roomId': 'eae5ad52-85ee-44c5-b0c3-1f6239cc0ffe',
    'preRoomId': 'f8f6b1ab-47a4-4ba2-86e2-71af5e751cf7',
}
headers = {
    'user-agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

data = {
    'csrfmiddlewaretoken': '',
    'username': ' ',
    'password': '',
    'next': '',
}


async def scrape_links(url, session):
    async with session.get(url, timeout=3500) as response:
        html = await response.text()

    soup = BeautifulSoup(html, "html.parser")

    try:
        links = []
        for a in soup.find_all('a', href=True):
            link = a['href']
            links.append(link)

        tasks = []
        for link in links:
            if link.startswith("/product") or link.startswith(
                    "https://terraceramica.ru"):
                link = link if link.startswith(
                    "https://terraceramica.ru"
                ) else "https://terraceramica.ru" + link
                if link not in visited_links:
                    visited_links.add(link)

                    if link.startswith("https://terraceramica.ru/product/"):
                        print(link)
                        # tasks.append(asyncio.create_task(scrape_products(link, session)))
                        with open(f'links.txt', 'a') as f:
                            f.write(link + '\n')

                    tasks.append(asyncio.create_task(
                        scrape_links(link, session)))

        await asyncio.gather(*tasks)
    except:
        print('*'*20)
        print('thats all! \nrun main.py file')
        print('*'*20)


start_url = "https://terraceramica.ru/"
visited_links = set([start_url])


async def main():
    async with aiohttp.ClientSession() as session:
        await scrape_links(start_url, session)


if __name__ == '__main__':
    asyncio.run(main())
