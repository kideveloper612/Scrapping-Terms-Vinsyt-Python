import requests
import os
import csv
import time
from bs4 import BeautifulSoup
from urllib.parse import unquote
import re
import json


def send_request(url, method='GET', payload={}):
    global s
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    return s.request(method, url=url, headers=headers, data=payload)


def parse(html):
    return BeautifulSoup(html, 'html5lib')


def main():
    land = send_request(url=landing_url)
    csrf = parse(land.text).find(attrs={'name': '_csrf'})['value']
    auth_payload = {
        '_csrf': csrf,
        'LoginForm[username]': 'admin',
        'LoginForm[password]': 'C@rm@il09',
        'LoginForm[rememberMe]': 'off',
        'timezone': 'Asia/Shanghai'
    }
    send_request(method='POST', url=login_url, payload=auth_payload)
    report_soup = send_request(url=report_url)
    print(report_soup.text)


def read_txt():
    path = 'urls.txt'
    file = open(file=path, encoding='utf-8', mode='r')
    rows = file.readlines()
    file.close()
    return rows


def write_csv(lines, file_name):
    with open(file=file_name, encoding='utf-8', newline='', mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)


def loop():
    urls = read_txt()
    lines = []
    for url in urls:
        url = unquote(url)
        make = re.search('make=(.*)&year', url).group(1).strip()
        make_id = url.split('=')[-1].strip()
        for year in range(2015, 2022):
            new_url = 'https://app.vinsyt.com/report-model/get-model-list?make={}&year={}&make_id={}'.format(make, year, make_id)
            new_res = send_request(url=new_url).json()
            for res in new_res:
                model = res['description']
                feature = res['image']
                how_to = res['video']
                gallery = res['gallery']
                pdf = res['pdf']
                # if '0' in str(feature) and '0' in str(how_to) and '0' in str(gallery) and '0' in str(pdf):
                #     continue
                line = [year, make, model, feature, how_to, gallery, pdf]
                if line not in lines:
                    lines.append(line)
                print(line)
    lines.sort(key=lambda x: x[0])
    write_csv(lines=lines, file_name=file_name)


if __name__ == '__main__':
    print('----- Start -----')
    username = 'admin'
    password = 'C@rm@il09'
    s = requests.Session()
    landing_url = 'https://app.vinsyt.com'
    login_url = 'https://app.vinsyt.com/site/login'
    report_url = 'https://app.vinsyt.com/report-model'
    file_name = 'Result.csv'
    csv_header = [['YEAR', 'MAKE', 'MODEL', 'FEATURES', 'HOW TO VIDEOS', 'GALLERY', 'PDF']]
    write_csv(lines=csv_header, file_name=file_name)
    loop()
    print('---- The End ----')