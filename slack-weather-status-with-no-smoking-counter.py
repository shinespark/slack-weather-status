# coding: utf-8
from bs4 import BeautifulSoup
import datetime
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
        '02': ':mostly_sunny:',
        '03': ':partly_sunny_lain:',
        '04': ':snow_cloud:',
        '05': ':partly_sunny:',
        '06': ':partly_sunny_lain:',
        '07': ':snow_cloud:',
        '08': ':cloud:',
        '09': ':partly_sunny:',
        '10': ':rain_cloud:',
        '11': ':snow_cloud:',
        '12': ':partly_sunny:',
        '13': ':rain_cloud:',
        '14': ':snow_cloud:',
        '15': ':umbrella:',
        '16': ':rain_cloud:',
        '17': ':umbrella:',
        '18': ':umbrella:',
        '19': ':umbrella:',
        '20': ':rain_cloud:',
        '21': ':rain_cloud:',
        '22': ':rain_cloud:',
        '23': ':snowman_without_snow:',
        '24': ':snowman_without_snow:',
        '25': ':snowman_without_snow:',
        '26': ':snowman_without_snow:',
        '27': ':snowman_without_snow:',
        '28': ':snowman_without_snow:',
        '29': ':snowman_without_snow:',
        '30': ':snowman:',
    }

    icon = soup_today.find('div', 'weather-icon').find('img')
    icon_png = icon['src'].split('/')[-1].rstrip('_n.png')
    now = datetime.datetime.now()
    text = icon['title']

    if icon_png in icon_d:
        emoji = icon_d[icon_png]
    else:
        emoji = ':question:'
        text = icon_png + text

    text += ', {}{}'.format(soup_today.find('dd', 'low-temp').get_text(), soup_today.find('dd', 'low-temp tempdiff').string)
    text += ' 〜 {}{}'.format(soup_today.find('dd', 'high-temp').get_text(), soup_today.find('dd', 'high-temp tempdiff').string)
    if 'no_smoking' in conf:
        no_smoking_days = (now - datetime.datetime.strptime(conf['no_smoking']['started_at'], '%Y/%m/%d')).days
        text = ', :no_smoking:: {}日目, {}本, {}円'.format(no_smoking_days, no_smoking_days * 20, no_smoking_days * 460) + text
    text += ', 取得: {}'.format(now.strftime("%H:%M"))

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
