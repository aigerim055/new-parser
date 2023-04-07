import datetime
from bs4 import BeautifulSoup
import time
import xlsxwriter
import asyncio
import aiohttp

start_time = time.time()
result = []
cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

cookies = {
    'csrftoken': '38LU3tgTgto1PsaoIKjCNTDftxri2Pxrnb0AbnemmOKcA0Xp7pxg7h4dchdntUAg',
    'sessionid': '9tp28dt3d0j77m4wsf2tmijzpkcye9us',
    'is_authenticated': '1',
    'roomId': 'eae5ad52-85ee-44c5-b0c3-1f6239cc0ffe',
    'preRoomId': 'f8f6b1ab-47a4-4ba2-86e2-71af5e751cf7',
}
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

data = {
    'csrfmiddlewaretoken': '',
    'username': ' ',
    'password': '',
    'next': '',
}

OUT_XLSX_FILENAME = f'catalog_{cur_time}.xlsx'


async def get_page_data(session):
    with open('links.txt') as f:
        links = f.readlines()
        for link in links:
            response = await session.get(url=link, data=data, headers=headers, timeout=3000)
            soup = BeautifulSoup(await response.text(), "lxml")

            try:
                image = soup.find(
                    'div', class_="col-12 col-md-6 col-lg-5 d-flex").find('img').get('src')
                image = f'https://terraceramica.ru{image}'
            except AttributeError:
                image = ''

            try:
                code = soup.find('div', class_='item_details_article').find(
                    'div', class_='value').text
            except AttributeError:
                code = ''

            try:
                title = soup.find('h1').text
            except AttributeError:
                title = ''

            try:
                price = soup.find(
                    'div', class_="item_details_price_val").text.strip('₽/кв.м.')
            except AttributeError:
                price = ''

            try:
                price_q = soup.find(
                    'div', class_="item_details_price_val").find('span').text
            except AttributeError:
                price_q = ''

            try:
                price_without_discount = soup.find('div', class_="item_details_price_val_base").find('div',
                                                                                                     class_='value').text.strip(
                    '₽/кв.м.')
            except AttributeError:
                price_without_discount = ''

            try:
                price_without_discount_q = soup.find('div', class_="item_details_price_val_base").find('div',
                                                                                                       class_='value').find(
                    'span').text
            except AttributeError:
                price_without_discount_q = ''

            try:
                info = soup.find('div', class_="item_details_info").find_all('div',
                                                                             class_='item')  # .find('div', class_='value').text
            except AttributeError:
                info = ''

            try:
                articul = info[0].find('div', class_='value').text
            except (AttributeError, IndexError):
                articul = ''

            try:
                collection = info[1].find('a').text
            except (AttributeError, IndexError):
                collection = ''

            try:
                manufacture = info[2].find('a').text
            except (AttributeError, IndexError):
                manufacture = ''

            try:
                color = info[3].find('div', class_='value').text
            except (AttributeError, IndexError):
                color = ''

            try:
                size = info[4].find('div', class_='value').text
            except (AttributeError, IndexError):
                size = ''

            try:
                thickness = info[5].find('div', class_='value').text
            except (AttributeError, IndexError):
                thickness = ''

            try:
                in_stock_cards = soup.find(
                    'div', class_='table_container').find_all('tr')
            except AttributeError:
                in_stock_cards = ''

            try:
                in_stock_1 = in_stock_cards[0].find('div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_1 = ''

            try:
                in_stock_1_tone = in_stock_cards[0].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_1_tone = ''

            try:
                in_stock_1_caliber = in_stock_cards[0].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_1_caliber = ''

            try:
                in_stock_1_cost = in_stock_cards[0].find('div', class_='cost').find('span').text.strip(
                    'кв.м.')  # остаток
            except (AttributeError, IndexError):
                in_stock_1_cost = ''

            try:
                in_stock_1_cost_q = in_stock_cards[0].find(
                    'div', class_='cost').find('span').text[-6:]  # остаток
            except (AttributeError, IndexError):
                in_stock_1_cost_q = ''

            try:
                in_stock_2 = in_stock_cards[1].find('div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_2 = ''

            try:
                in_stock_2_tone = in_stock_cards[1].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_2_tone = ''

            try:
                in_stock_2_caliber = in_stock_cards[1].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_2_caliber = ''

            try:
                in_stock_2_cost = in_stock_cards[1].find(
                    'div', class_='cost').find('span').text.strip('кв.м.')
            except (AttributeError, IndexError):
                in_stock_2_cost = ''

            try:
                in_stock_2_cost_q = in_stock_cards[1].find(
                    'div', class_='cost').find('span').text[-6:]
            except (AttributeError, IndexError):
                in_stock_2_cost_q = ''

            try:
                in_stock_3 = in_stock_cards[2].find('div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_3 = ''

            try:
                in_stock_3_tone = in_stock_cards[2].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_3_tone = ''

            try:
                in_stock_3_caliber = in_stock_cards[2].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_3_caliber = ''

            try:
                in_stock_3_cost = in_stock_cards[2].find(
                    'div', class_='cost').find('span').text.strip('кв.м.')
            except (AttributeError, IndexError):
                in_stock_3_cost = ''

            try:
                in_stock_3_cost_q = in_stock_cards[2].find(
                    'div', class_='cost').find('span').text[-6:]
            except (AttributeError, IndexError):
                in_stock_3_cost_q = ''

            try:
                in_stock_4 = in_stock_cards[3].find('div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_4 = ''

            try:
                in_stock_4_tone = in_stock_cards[3].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_4_tone = ''

            try:
                in_stock_4_caliber = in_stock_cards[3].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_4_caliber = ''

            try:
                in_stock_4_cost = in_stock_cards[3].find(
                    'div', class_='cost').find('span').text.strip('кв.м.')
            except (AttributeError, IndexError):
                in_stock_4_cost = ''

            try:
                in_stock_4_cost_q = in_stock_cards[3].find(
                    'div', class_='cost').find('span').text[-6:]
            except (AttributeError, IndexError):
                in_stock_4_cost_q = ''

            try:
                in_stock_5 = in_stock_cards[4].find('div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_5 = ''

            try:
                in_stock_5_tone = in_stock_cards[4].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_5_tone = ''

            try:
                in_stock_5_caliber = in_stock_cards[4].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_5_caliber = ''

            try:
                in_stock_5_cost = in_stock_cards[4].find(
                    'div', class_='cost').find('span').text.strip('кв.м.')
            except (AttributeError, IndexError):
                in_stock_5_cost = ''

            try:
                in_stock_5_cost_q = in_stock_cards[4].find(
                    'div', class_='cost').find('span').text[-6:]
            except (AttributeError, IndexError):
                in_stock_5_cost_q = ''

            try:
                in_stock_6 = in_stock_cards[5].find('div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_6 = ''

            try:
                in_stock_6_tone = in_stock_cards[5].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_6_tone = ''

            try:
                in_stock_6_caliber = in_stock_cards[5].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_6_caliber = ''

            try:
                in_stock_6_cost = in_stock_cards[5].find(
                    'div', class_='cost').find('span').text.strip('кв.м.')
            except (AttributeError, IndexError):
                in_stock_6_cost = ''

            try:
                in_stock_6_cost_q = in_stock_cards[5].find(
                    'div', class_='cost').find('span').text[-6:]
            except (AttributeError, IndexError):
                in_stock_6_cost_q = ''

            try:
                in_stock_7 = in_stock_cards[6].find('div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_7 = ''

            try:
                in_stock_7_tone = in_stock_cards[6].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_7_tone = ''

            try:
                in_stock_7_caliber = in_stock_cards[6].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_7_caliber = ''

            try:
                in_stock_7_cost = in_stock_cards[6].find(
                    'div', class_='cost').find('span').text.strip('кв.м.')
            except (AttributeError, IndexError):
                in_stock_7_cost = ''

            try:
                in_stock_7_cost_q = in_stock_cards[6].find(
                    'div', class_='cost').find('span').text[-6:]
            except (AttributeError, IndexError):
                in_stock_7_cost_q = ''

            try:
                in_stock_8 = in_stock_cards[7].find('div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_8 = ''

            try:
                in_stock_8_tone = in_stock_cards[7].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_8_tone = ''

            try:
                in_stock_8_caliber = in_stock_cards[7].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_8_caliber = ''

            try:
                in_stock_8_cost = in_stock_cards[7].find(
                    'div', class_='cost').find('span').text.strip('кв.м.')
            except (AttributeError, IndexError):
                in_stock_8_cost = ''

            try:
                in_stock_8_cost_q = in_stock_cards[7].find(
                    'div', class_='cost').find('span').text[-6:]
            except (AttributeError, IndexError):
                in_stock_8_cost_q = ''

            try:
                in_stock_9 = in_stock_cards[8].find('div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_9 = ''

            try:
                in_stock_9_tone = in_stock_cards[8].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_9_tone = ''

            try:
                in_stock_9_caliber = in_stock_cards[8].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_9_caliber = ''

            try:
                in_stock_9_cost = in_stock_cards[8].find(
                    'div', class_='cost').find('span').text.strip('кв.м.')
            except (AttributeError, IndexError):
                in_stock_9_cost = ''

            try:
                in_stock_9_cost_q = in_stock_cards[8].find(
                    'div', class_='cost').find('span').text[-6:]
            except (AttributeError, IndexError):
                in_stock_9_cost_q = ''

            try:
                in_stock_10 = in_stock_cards[9].find(
                    'div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_10 = ''

            try:
                in_stock_10_tone = in_stock_cards[9].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_10_tone = ''

            try:
                in_stock_10_caliber = in_stock_cards[9].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_10_caliber = ''

            try:
                in_stock_10_cost = in_stock_cards[9].find(
                    'div', class_='cost').find('span').text.strip('кв.м.')
            except (AttributeError, IndexError):
                in_stock_10_cost = ''

            try:
                in_stock_10_cost_q = in_stock_cards[9].find(
                    'div', class_='cost').find('span').text[-6:]
            except (AttributeError, IndexError):
                in_stock_10_cost_q = ''

            try:
                in_stock_11 = in_stock_cards[10].find(
                    'div', class_='stock').text
            except (AttributeError, IndexError):
                in_stock_11 = ''

            try:
                in_stock_11_tone = in_stock_cards[10].find(
                    'div', class_='tone').find('span').text
            except (AttributeError, IndexError):
                in_stock_11_tone = ''

            try:
                in_stock_11_caliber = in_stock_cards[10].find(
                    'div', class_='caliber').find('span').text
            except (AttributeError, IndexError):
                in_stock_11_caliber = ''

            try:
                in_stock_11_cost = in_stock_cards[10].find(
                    'div', class_='cost').find('span').text.strip('кв.м.')
            except (AttributeError, IndexError):
                in_stock_11_cost = ''

            try:
                in_stock_11_cost_q = in_stock_cards[10].find(
                    'div', class_='cost').find('span').text[-6:]
            except (AttributeError, IndexError):
                in_stock_11_cost_q = ''

            try:
                packing_cards = soup.find(
                    'div', class_="item_details_props").find_all('div', class_='item')
            except AttributeError:
                packing_cards = ''

            try:
                packing_quantity = packing_cards[0].find(
                    'div', class_='value').text
            except (AttributeError, IndexError):
                packing_quantity = ''

            try:
                packing_quantity_in_poddon = packing_cards[1].find(
                    'div', class_='value').text
            except (AttributeError, IndexError):
                packing_quantity_in_poddon = ''

            try:
                packing_m2 = packing_cards[2].find('div', class_='value').text
            except (AttributeError, IndexError):
                packing_m2 = ''

            try:
                packing_m2_on_poddon = packing_cards[3].find(
                    'div', class_='value').text
            except (AttributeError, IndexError):
                packing_m2_on_poddon = ''

            try:
                weight_poddon = packing_cards[4].find(
                    'div', class_='value').text
            except (AttributeError, IndexError):
                weight_poddon = ''

            try:
                weight_pack = packing_cards[5].find('div', class_='value').text
            except (AttributeError, IndexError):
                weight_pack = ''

            try:
                characteristics_cards = soup.find_all('div', class_="item_details_props")[1].find_all('div',
                                                                                                      class_='item')
            except (AttributeError, IndexError):
                characteristics_cards = ''

            try:
                haracteristics_1 = characteristics_cards[0].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_1 = ''

            try:
                haracteristics_1_q = characteristics_cards[0].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_1_q = ''

            try:
                haracteristics_2 = characteristics_cards[1].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_2 = ''

            try:
                haracteristics_2_q = characteristics_cards[1].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_2_q = ''

            try:
                haracteristics_3 = characteristics_cards[2].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_3 = ''

            try:
                haracteristics_3_q = characteristics_cards[2].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_3_q = ''

            try:
                haracteristics_4 = characteristics_cards[3].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_4 = ''

            try:
                haracteristics_4_q = characteristics_cards[3].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_4_q = ''

            try:
                haracteristics_5 = characteristics_cards[4].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_5 = ''

            try:
                haracteristics_5_q = characteristics_cards[4].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_5_q = ''

            try:
                haracteristics_6 = characteristics_cards[5].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_6 = ''

            try:
                haracteristics_6_q = characteristics_cards[5].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_6_q = ''

            try:
                haracteristics_7 = characteristics_cards[6].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_7 = ''

            try:
                haracteristics_7_q = characteristics_cards[6].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_7_q = ''

            try:
                haracteristics_8 = characteristics_cards[7].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_8 = ''

            try:
                haracteristics_8_q = characteristics_cards[7].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_8_q = ''

            try:
                haracteristics_9 = characteristics_cards[8].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_9 = ''

            try:
                haracteristics_9_q = characteristics_cards[8].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_9_q = ''

            try:
                haracteristics_10 = characteristics_cards[9].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_10 = ''

            try:
                haracteristics_10_q = characteristics_cards[9].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_10_q = ''

            try:
                haracteristics_11 = characteristics_cards[10].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_11 = ''

            try:
                haracteristics_11_q = characteristics_cards[10].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_11_q = ''

            try:
                haracteristics_12 = characteristics_cards[11].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_12 = ''

            try:
                haracteristics_12_q = characteristics_cards[11].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_12_q = ''

            try:
                haracteristics_13 = characteristics_cards[12].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_13 = ''

            try:
                haracteristics_13_q = characteristics_cards[12].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_13_q = ''

            try:
                haracteristics_14 = characteristics_cards[13].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_14 = ''

            try:
                haracteristics_14_q = characteristics_cards[13].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_14_q = ''

            try:
                haracteristics_15 = characteristics_cards[14].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_15 = ''

            try:
                haracteristics_15_q = characteristics_cards[14].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_15_q = ''

            try:
                haracteristics_16 = characteristics_cards[15].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_16 = ''

            try:
                haracteristics_16_q = characteristics_cards[15].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_16_q = ''

            try:
                haracteristics_17 = characteristics_cards[16].find(
                    'div', class_='subtext').text.strip() + ':'
            except (AttributeError, IndexError):
                haracteristics_17 = ''

            try:
                haracteristics_17_q = characteristics_cards[16].find(
                    'div', class_='value').text.strip()
            except (AttributeError, IndexError):
                haracteristics_17_q = ''

            obj = {

                'image': image,
                'code': code,
                'title': title,
                'price': price,
                'price_q': price_q,
                'price_without_discount': price_without_discount,  # цена без скидки
                'price_without_discount_q': price_without_discount_q,
                'articul': articul,
                'collection': collection,
                'manufacture': manufacture,  # производитель
                'color': color,
                'size': size,
                'thickness': thickness,  # толщина

                'in_stock_1': in_stock_1,
                'in_stock_1_tone': in_stock_1_tone,
                'in_stock_1_caliber': in_stock_1_caliber,
                'in_stock_1_cost': in_stock_1_cost,
                'in_stock_1_cost_q': in_stock_1_cost_q,

                'in_stock_2': in_stock_2,
                'in_stock_2_tone': in_stock_2_tone,
                'in_stock_2_caliber': in_stock_2_caliber,
                'in_stock_2_cost': in_stock_2_cost,
                'in_stock_2_cost_q': in_stock_2_cost_q,

                'in_stock_3': in_stock_3,
                'in_stock_3_tone': in_stock_3_tone,
                'in_stock_3_caliber': in_stock_3_caliber,
                'in_stock_3_cost': in_stock_3_cost,
                'in_stock_3_cost_q': in_stock_3_cost_q,

                'in_stock_4': in_stock_4,
                'in_stock_4_tone': in_stock_4_tone,
                'in_stock_4_caliber': in_stock_4_caliber,
                'in_stock_4_cost': in_stock_4_cost,
                'in_stock_4_cost_q': in_stock_4_cost_q,

                'in_stock_5': in_stock_5,
                'in_stock_5_tone': in_stock_5_tone,
                'in_stock_5_caliber': in_stock_5_caliber,
                'in_stock_5_cost': in_stock_5_cost,
                'in_stock_5_cost_q': in_stock_5_cost_q,

                'in_stock_6': in_stock_6,
                'in_stock_6_tone': in_stock_6_tone,
                'in_stock_6_caliber': in_stock_6_caliber,
                'in_stock_6_cost': in_stock_6_cost,
                'in_stock_6_cost_q': in_stock_6_cost_q,

                'in_stock_7': in_stock_7,
                'in_stock_7_tone': in_stock_7_tone,
                'in_stock_7_caliber': in_stock_7_caliber,
                'in_stock_7_cost': in_stock_7_cost,
                'in_stock_7_cost_q': in_stock_7_cost_q,

                'in_stock_8': in_stock_8,
                'in_stock_8_tone': in_stock_8_tone,
                'in_stock_8_caliber': in_stock_8_caliber,
                'in_stock_8_cost': in_stock_8_cost,
                'in_stock_8_cost_q': in_stock_8_cost_q,

                'in_stock_9': in_stock_9,
                'in_stock_9_tone': in_stock_9_tone,
                'in_stock_9_caliber': in_stock_9_caliber,
                'in_stock_9_cost': in_stock_9_cost,
                'in_stock_9_cost_q': in_stock_9_cost_q,

                'in_stock_10': in_stock_10,
                'in_stock_10_tone': in_stock_10_tone,
                'in_stock_10_caliber': in_stock_10_caliber,
                'in_stock_10_cost': in_stock_10_cost,
                'in_stock_10_cost_q': in_stock_10_cost_q,

                'in_stock_11': in_stock_11,
                'in_stock_11_tone': in_stock_11_tone,
                'in_stock_11_caliber': in_stock_11_caliber,
                'in_stock_11_cost': in_stock_11_cost,
                'in_stock_11_cost_q': in_stock_11_cost_q,

                'packing_quantity': packing_quantity,  # количество в упаковке
                # Количество упаковок на поддоне
                'packing_quantity_in_poddon': packing_quantity_in_poddon,
                'packing_m2': packing_m2,  # M2 в упаковке
                'packing_m2_on_poddon': packing_m2_on_poddon,  # M2 на поддоне
                'weight_poddon': weight_poddon,  # Вес поддона
                'weight_pack': weight_pack,  # Вес упаковки

                'haracteristics_1': haracteristics_1,
                'haracteristics_1_q': haracteristics_1_q,

                'haracteristics_2': haracteristics_2,
                'haracteristics_2_q': haracteristics_2_q,

                'haracteristics_3': haracteristics_3,
                'haracteristics_3_q': haracteristics_3_q,

                'haracteristics_4': haracteristics_4,
                'haracteristics_4_q': haracteristics_4_q,

                'haracteristics_5': haracteristics_5,
                'haracteristics_5_q': haracteristics_5_q,

                'haracteristics_6': haracteristics_6,
                'haracteristics_6_q': haracteristics_6_q,

                'haracteristics_7': haracteristics_7,
                'haracteristics_7_q': haracteristics_7_q,

                'haracteristics_8': haracteristics_8,
                'haracteristics_8_q': haracteristics_8_q,

                'haracteristics_9': haracteristics_9,
                'haracteristics_9_q': haracteristics_9_q,

                'haracteristics_10': haracteristics_10,
                'haracteristics_10_q': haracteristics_10_q,

                'haracteristics_11': haracteristics_11,
                'haracteristics_11_q': haracteristics_11_q,

                'haracteristics_12': haracteristics_12,
                'haracteristics_12_q': haracteristics_12_q,

                'haracteristics_13': haracteristics_13,
                'haracteristics_13_q': haracteristics_13_q,

                'haracteristics_14': haracteristics_14,
                'haracteristics_14_q': haracteristics_14_q,

                'haracteristics_15': haracteristics_15,
                'haracteristics_15_q': haracteristics_15_q,

                'haracteristics_16': haracteristics_16,
                'haracteristics_16_q': haracteristics_16_q,

                'haracteristics_17': haracteristics_17,
                'haracteristics_17_q': haracteristics_17_q,

            }
            result.append(obj)
            write_to_excel(OUT_XLSX_FILENAME, result)
            print(f"[INFO] Обработал товар - {title}")


OUT_XLSX_FILENAME = f'catalog_{cur_time}.xlsx'


def write_to_excel(file_name, data):
    """ Запись данных в xlsx файл """
    if not len(data):
        return None

    with xlsxwriter.Workbook(file_name) as workbook:
        ws = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        titles = ['картинка', 'код', 'наименование', 'цена', 'размерность цены', 'цена без скидки',
                  'размерность цены без скидки', 'артикул', 'коллекция', 'производитель', 'цвет', 'размер', 'толщина',

                  'наличие в магазине №1', 'тон', 'калибр', 'остаток', 'размерность остатка',
                  'наличие в магазине №2', 'тон', 'калибр', 'остаток', 'размерность остатка',
                  'наличие в магазине №3', 'тон', 'калибр', 'остаток', 'размерность остатка',
                  'наличие в магазине №4', 'тон', 'калибр', 'остаток', 'размерность остатка',
                  'наличие в магазине №5', 'тон', 'калибр', 'остаток', 'размерность остатка',
                  'наличие в магазине №6', 'тон', 'калибр', 'остаток', 'размерность остатка',
                  'наличие в магазине №7', 'тон', 'калибр', 'остаток', 'размерность остатка',
                  'наличие в магазине №8', 'тон', 'калибр', 'остаток', 'размерность остатка',
                  'наличие в магазине №9', 'тон', 'калибр', 'остаток', 'размерность остатка',
                  'наличие в магазине №10', 'тон', 'калибр', 'остаток', 'размерность остатка',
                  'наличие в магазине №11', 'тон', 'калибр', 'остаток', 'размерность остатка',

                  'количество в упаковке', 'количество упаковок на поддоне', 'M2 в упаковке', 'M2 на поддоне',
                  'вес поддона', 'вес упаковки',

                  'название характеристики', 'значение характеристики', 'название характеристики',
                  'значение характеристики',
                  'название характеристики', 'значение характеристики', 'название характеристики',
                  'значение характеристики',
                  'название характеристики', 'значение характеристики', 'название характеристики',
                  'значение характеристики',
                  'название характеристики', 'значение характеристики', 'название характеристики',
                  'значение характеристики',
                  'название характеристики', 'значение характеристики', 'название характеристики',
                  'значение характеристики',
                  'название характеристики', 'значение характеристики', 'название характеристики',
                  'значение характеристики',
                  'название характеристики', 'значение характеристики', 'название характеристики',
                  'значение характеристики',
                  'название характеристики', 'значение характеристики', 'название характеристики',
                  'значение характеристики',
                  'название характеристики', 'значение характеристики',

                  ]

        for col, h in enumerate(titles):
            ws.write_string(0, col, h, cell_format=bold)

            for row, item in enumerate(data, start=1):
                ws.write_string(row, 0, item['image'])
                ws.write_string(row, 1, item['code'])
                ws.write_string(row, 2, item['title'])
                ws.write_string(row, 3, item['price'])
                ws.write_string(row, 4, item['price_q'])
                ws.write_string(row, 5, item['price_without_discount'])
                ws.write_string(row, 6, item['price_without_discount_q'])
                ws.write_string(row, 7, item['articul'])
                ws.write_string(row, 8, item['collection'])
                ws.write_string(row, 9, item['manufacture'])
                ws.write_string(row, 10, item['color'])
                ws.write_string(row, 11, item['size'])
                ws.write_string(row, 12, item['thickness'])

                ws.write_string(row, 13, item['in_stock_1'])
                ws.write_string(row, 14, item['in_stock_1_tone'])
                ws.write_string(row, 15, item['in_stock_1_caliber'])
                ws.write_string(row, 16, item['in_stock_1_cost'])
                ws.write_string(row, 17, item['in_stock_1_cost_q'])

                ws.write_string(row, 18, item['in_stock_2'])
                ws.write_string(row, 19, item['in_stock_2_tone'])
                ws.write_string(row, 20, item['in_stock_2_caliber'])
                ws.write_string(row, 21, item['in_stock_2_cost'])
                ws.write_string(row, 22, item['in_stock_2_cost_q'])

                ws.write_string(row, 23, item['in_stock_3'])
                ws.write_string(row, 24, item['in_stock_3_tone'])
                ws.write_string(row, 25, item['in_stock_3_caliber'])
                ws.write_string(row, 26, item['in_stock_3_cost'])
                ws.write_string(row, 27, item['in_stock_3_cost_q'])

                ws.write_string(row, 28, item['in_stock_4'])
                ws.write_string(row, 29, item['in_stock_4_tone'])
                ws.write_string(row, 30, item['in_stock_4_caliber'])
                ws.write_string(row, 31, item['in_stock_4_cost'])
                ws.write_string(row, 32, item['in_stock_4_cost_q'])

                ws.write_string(row, 33, item['in_stock_5'])
                ws.write_string(row, 34, item['in_stock_5_tone'])
                ws.write_string(row, 35, item['in_stock_5_caliber'])
                ws.write_string(row, 36, item['in_stock_5_cost'])
                ws.write_string(row, 37, item['in_stock_5_cost_q'])

                ws.write_string(row, 38, item['in_stock_6'])
                ws.write_string(row, 39, item['in_stock_6_tone'])
                ws.write_string(row, 40, item['in_stock_6_caliber'])
                ws.write_string(row, 41, item['in_stock_6_cost'])
                ws.write_string(row, 42, item['in_stock_6_cost_q'])

                ws.write_string(row, 43, item['in_stock_7'])
                ws.write_string(row, 44, item['in_stock_7_tone'])
                ws.write_string(row, 45, item['in_stock_7_caliber'])
                ws.write_string(row, 46, item['in_stock_7_cost'])
                ws.write_string(row, 47, item['in_stock_7_cost_q'])

                ws.write_string(row, 48, item['in_stock_8'])
                ws.write_string(row, 49, item['in_stock_8_tone'])
                ws.write_string(row, 50, item['in_stock_8_caliber'])
                ws.write_string(row, 51, item['in_stock_8_cost'])
                ws.write_string(row, 52, item['in_stock_8_cost_q'])

                ws.write_string(row, 53, item['in_stock_9'])
                ws.write_string(row, 54, item['in_stock_9_tone'])
                ws.write_string(row, 55, item['in_stock_9_caliber'])
                ws.write_string(row, 56, item['in_stock_9_cost'])
                ws.write_string(row, 57, item['in_stock_9_cost_q'])

                ws.write_string(row, 58, item['in_stock_10'])
                ws.write_string(row, 59, item['in_stock_10_tone'])
                ws.write_string(row, 60, item['in_stock_10_caliber'])
                ws.write_string(row, 61, item['in_stock_10_cost'])
                ws.write_string(row, 62, item['in_stock_10_cost_q'])

                ws.write_string(row, 63, item['in_stock_11'])
                ws.write_string(row, 64, item['in_stock_11_tone'])
                ws.write_string(row, 65, item['in_stock_11_caliber'])
                ws.write_string(row, 66, item['in_stock_11_cost'])
                ws.write_string(row, 67, item['in_stock_11_cost_q'])

                ws.write_string(row, 68, item['packing_quantity'])
                ws.write_string(row, 69, item['packing_quantity_in_poddon'])
                ws.write_string(row, 70, item['packing_m2'])
                ws.write_string(row, 71, item['packing_m2_on_poddon'])
                ws.write_string(row, 72, item['weight_poddon'])
                ws.write_string(row, 73, item['weight_pack'])

                ws.write_string(row, 74, item['haracteristics_1'])
                ws.write_string(row, 75, item['haracteristics_1_q'])
                ws.write_string(row, 76, item['haracteristics_2'])
                ws.write_string(row, 77, item['haracteristics_2_q'])
                ws.write_string(row, 78, item['haracteristics_3'])
                ws.write_string(row, 79, item['haracteristics_3_q'])
                ws.write_string(row, 80, item['haracteristics_4'])
                ws.write_string(row, 81, item['haracteristics_4_q'])
                ws.write_string(row, 82, item['haracteristics_5'])
                ws.write_string(row, 83, item['haracteristics_5_q'])
                ws.write_string(row, 84, item['haracteristics_6'])
                ws.write_string(row, 85, item['haracteristics_6_q'])
                ws.write_string(row, 86, item['haracteristics_7'])
                ws.write_string(row, 87, item['haracteristics_7_q'])
                ws.write_string(row, 88, item['haracteristics_8'])
                ws.write_string(row, 89, item['haracteristics_8_q'])
                ws.write_string(row, 90, item['haracteristics_9'])
                ws.write_string(row, 91, item['haracteristics_9_q'])
                ws.write_string(row, 92, item['haracteristics_10'])
                ws.write_string(row, 93, item['haracteristics_10_q'])
                ws.write_string(row, 94, item['haracteristics_11'])
                ws.write_string(row, 95, item['haracteristics_11_q'])
                ws.write_string(row, 96, item['haracteristics_12'])
                ws.write_string(row, 97, item['haracteristics_12_q'])
                ws.write_string(row, 98, item['haracteristics_13'])
                ws.write_string(row, 99, item['haracteristics_13_q'])
                ws.write_string(row, 100, item['haracteristics_14'])
                ws.write_string(row, 101, item['haracteristics_14_q'])
                ws.write_string(row, 102, item['haracteristics_15'])
                ws.write_string(row, 103, item['haracteristics_15_q'])
                ws.write_string(row, 104, item['haracteristics_16'])
                ws.write_string(row, 105, item['haracteristics_16_q'])
                ws.write_string(row, 106, item['haracteristics_17'])
                ws.write_string(row, 107, item['haracteristics_17_q'])


async def gather_data():
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        task = asyncio.create_task(get_page_data(session))
        tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())
    # write_to_excel(OUT_XLSX_FILENAME, result)
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == "__main__":
    main()
