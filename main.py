import time
import gspread
import requests
from bs4 import BeautifulSoup

while True:
    gc = gspread.service_account(filename="telegram-314312-7965025b5a7f.json")
    sh = gc.open_by_key('17RkJmcG0ITS2Zp0hq17jJZ0uAOjC1zou_HVWmn4LlmI')
    worksheet = sh.get_worksheet(0)
    telegram_list = worksheet.col_values(1)[1:]
    avatars = []
    tittles = []
    subscribers_counts = []
    abouts = []

    for url in telegram_list:
        try:
            url = url[:13] + "s/" + url[13:]
            bs = BeautifulSoup(requests.get(
                url).text, "html.parser")

            tittle = bs.select("span[dir='auto']")[
                0].text if bs.select("span[dir='auto']") else ""

            subscribers_count = bs.select(".counter_value")[
                0].text if bs.select(".counter_value") else ""
            about = bs.select(".tgme_channel_info_description")[0].text if bs.select(
                ".tgme_channel_info_description") else ""
            avatar = bs.select(".tgme_page_photo_image")[
                0].select("img")[0].get("src") if bs.select(".tgme_page_photo_image")[0].select("img") else ""

            avatars.append(avatar)
            tittles.append(tittle)
            subscribers_counts.append(subscribers_count)
            abouts.append(about)
        except:
            print(url)

    columns = ["B", "C", "D", "E"]
    for c_n in columns:
        cell_list = worksheet.range(
            c_n + '2:' + c_n + str(len(telegram_list) + 1))
        if(c_n == "B"):
            c_v = avatars
        if(c_n == "C"):
            c_v = tittles
        if(c_n == "D"):
            c_v = subscribers_counts
        if(c_n == "E"):
            c_v = abouts
        for i, val in enumerate(c_v):
            cell_list[i].value = val
        worksheet.update_cells(cell_list)
    time.sleep(3600)
