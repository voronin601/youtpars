from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import re
import json
from django.http import HttpRequest
from apscheduler.scheduler import Scheduler
import time
from .models import data

# Create your views here.
def start_pars(requests):
    a = starts()
    a.start()
    return redirect('http://127.0.0.1:8000/')

def vivod(requests):
    return render(requests, 'start.html', context = {'data':data.objects.all(), 'len':data.objects.all().count()})

class starts:
    def __init__(self):
        self.start_url = 'https://www.youtube.com/feed/trending'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'content-type':'application/json'
        }
        self.name = {}
        self.sched = Scheduler()
        self.sched.start()
        self.sched.add_cron_job(self.db, minute = 5)

    def start(self):
        r = requests.get(self.start_url, headers = self.headers)
        url = []
        q = json.loads(r.text.split('window["ytInitialData"] = ')[1].split('    window["ytInitialPlayerResponse"] = ')[0][:-2])
        for i in range(len(q['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['expandedShelfContentsRenderer']['items'])):
            if q['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['expandedShelfContentsRenderer']['items'][i]['videoRenderer']['longBylineText']['runs'][0]['text'] not in self.name:
                self.name[q['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['expandedShelfContentsRenderer']['items'][i]['videoRenderer']['longBylineText']['runs'][0]['text']] = q['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['expandedShelfContentsRenderer']['items'][i]['videoRenderer']['longBylineText']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
                url.append('https://www.youtube.com' + q['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['expandedShelfContentsRenderer']['items'][i]['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'])
        while 1:
            url_new = self.next(url)
            url = url_new.copy()

    def next(self, urls):
        qwerty = 0
        url = []
        for idd, j in enumerate(urls):
            print(idd, len(urls), qwerty, len(self.name))
            r = requests.get(j, headers = self.headers)
            q = json.loads(r.text.split('window["ytInitialData"] = ')[1].split('    window["ytInitialPlayerResponse"] = ')[0][:-2])
            for i in range(len(q['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results'])):
                if 'compactVideoRenderer' in q['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results'][i]:
                    a = q['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results'][i]['compactVideoRenderer']['shortBylineText']['runs'][0]['text']
                    if a not in self.name.keys():
                        url.append('https://www.youtube.com' + q['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results'][i]['compactVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'])
                        self.name[a] = q['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results'][i]['compactVideoRenderer']['shortBylineText']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
                else: qwerty += 1
            time.sleep(10)
        return url

    def db(self):
        qwer = self.name.copy()
        for i in qwer:
            try:
                data.objects.get(name = i)
            except:
                try:
                    time.sleep(2)
                    r = requests.get('https://www.youtube.com' + qwer[i] + '/about')
                    q = json.loads(r.text.split('window["ytInitialData"] = ')[1].split('    window["ytInitialPlayerResponse"] = ')[0][:-2])
                    name = q['contents']['twoColumnBrowseResultsRenderer']['tabs'][5]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelAboutFullMetadataRenderer']['title']['simpleText']
                    try:
                        watch = int(''.join(q['contents']['twoColumnBrowseResultsRenderer']['tabs'][5]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelAboutFullMetadataRenderer']['viewCountText']['runs'][0]['text']).replace('\u00a0', ''))
                    except:
                        watch = int(''.join(q['contents']['twoColumnBrowseResultsRenderer']['tabs'][5]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelAboutFullMetadataRenderer']['viewCountText']['simpleText'].split(' ')[:-1]).replace('\u00a0', ''))
                    ava = q['contents']['twoColumnBrowseResultsRenderer']['tabs'][5]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelAboutFullMetadataRenderer']['avatar']['thumbnails'][0]['url']
                    try:
                        n = q['header']['c4TabbedHeaderRenderer']['subscriberCountText']['simpleText']
                    except:
                        try:
                            n = q['header']['c4TabbedHeaderRenderer']['subscriberCountText']['runs'][0]['text']
                        except:
                            n = q['contents']['twoColumnBrowseResultsRenderer']['tabs'][5]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelAboutFullMetadataRenderer']['viewCountText']['runs'][0]['text']
                    date = q['contents']['twoColumnBrowseResultsRenderer']['tabs'][5]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelAboutFullMetadataRenderer']['joinedDateText']['runs'][1]['text']
                    data.objects.create(name = name, n = n, date = date, watch = watch, ava = ava)
                    print("ADD %s" %name)
                except:
                    print("ERROR %s" %name)