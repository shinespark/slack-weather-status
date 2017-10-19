# coding: utf-8
from bs4 import BeautifulSoup
from datetime import datetime
import os
import urllib.parse
import urllib.request
import yaml


def main():
    dirpath = os.path.abspath(os.path.dirname(__file__))
    conf = yaml.load(open(dirpath + '/conf.yml').read())
    url = conf['weather_url']
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    soup_today = soup.find('section', 'today-weather')

    # テキトー
    icon_d = {
        '01': ':sunny:',
        '10': ':rain_cloud:',
        '15': ':umbrella:',
    }
    #  ':mostly_sunny:',
    #  ':partly_sunny:',
    #  ':barely_sunny:',
    #  ':partly_sunny_lain:',
    #  ':cloud:',
    #  ':rain_cloud:',
    #  ':thunder_cloud_and_rain:',
    #  ':lightning:',
    #  ':umbrella:',

    icon = soup_today.find('div', 'weather-icon').find('img')
    icon_png = icon['src'].split('/')[-1].rstrip('_n.png')
    text = icon['title']

    if icon_png in icon_d:
        emoji = icon_d[icon_png]
    else:
        emoji = ':question:'
        text = icon_png + text

    text = text + ' 最高: ' + soup_today.find('dd', 'high-temp').get_text() + soup_today.find('dd', 'high-temp tempdiff').string
    text = text + ' 最低: ' + soup_today.find('dd', 'low-temp').get_text() + soup_today.find('dd', 'low-temp tempdiff').string
    text = text + ' 取得: ' + datetime.now().strftime("%H:%M")

    params = urllib.parse.urlencode({
        'token': conf['token'],
        'profile': {
            'status_text': text,
            'status_emoji': emoji,
        },
    })
    params = params.encode('ascii')
    slack_url = 'https://slack.com/api/users.profile.set'
    req = urllib.request.Request(slack_url, params, {'Content-type': 'application/x-www-form-urlencoded'})
    urllib.request.urlopen(req)


if __name__ == "__main__":
    main()
