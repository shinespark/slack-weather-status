# coding: utf-8
from bs4 import BeautifulSoup
import os
import urllib.parse
import urllib.request
import yaml


def main():
    dirpath = os.path.abspath(os.path.dirname(__file__))
    conf = yaml.load(open(dirpath + '/conf.yml').read())
    url = conf['weather_url']
    atom = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(atom, 'lxml')

    # テキトー
    icon_d = {
        '01': ':sunny:',
        '02': ':mostly_sunny:',
        '03': ':partly_sunny:',
        '04': ':barely_sunny:',
        '05': ':partly_sunny_lain:',
        '06': ':cloud:',
        '07': ':rain_cloud:',
        '08': ':thunder_cloud_and_rain:',
        '09': ':lightning:',
        '10': ':umbrella:',
        '11': ':umbrella_with_rain_drops:',
    }

    soup_today = soup.find('section', 'today-weather')

    icon = soup_today.find('div', 'weather-icon').find('img')
    icon_png = icon['src'].lstrip('https://static.tenki.jp/images/icon/forecast-days-weather/').rstrip('.png').rstrip('_n')

    if icon_png in icon_d:
        emoji = icon_d[icon_png]
        text = ''
    else:
        emoji = ':question:'
        text = icon['title'] + ' '

    text = text + '最高' + soup_today.find('dd', 'high-temp').get_text() + soup_today.find('dd', 'high-temp tempdiff').string
    text = text + ' 最低' + soup_today.find('dd', 'low-temp').get_text() + soup_today.find('dd', 'low-temp tempdiff').string

    params = urllib.parse.urlencode({
        'token': conf['token'],
        'profile': {
            'status_text': text,
            'status_emoji': emoji,
        },
    })
    params = params.encode('ascii')
    slack_url = 'https://slack.com/api/users.profile.set'
    urllib.request.Request(slack_url, params, {'Content-type': 'application/x-www-form-urlencoded'})


if __name__ == "__main__":
    main()
