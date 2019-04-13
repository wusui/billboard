#!/usr/bin/python
# pylint: disable=W0223
"""
Scan the online Billbord Hot-100 pages and stash the data in a local
directory.

The directory will contain subdirectories for each year.
Each year will contain json files representing weeks that year.

The format of the week data will be in a list.  Each entry will be
a list consisting of the artist and the song title.  The top-level
list will be sorted in position on the Hot-100 order.
"""
import codecs
from html.parser import HTMLParser
from datetime import datetime
import os
import json
import sys
import requests

WEEK_URL = 'https://www.billboard.com/charts/hot-100/%s'
YEAR_URL = 'https://www.billboard.com/archive/charts/%s/hot-100'
START_YEAR = 1958

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class ParseWeek(HTMLParser):
    """
    Extract the data from a weekly chart
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = []
        self.title = ''
        self.artist = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for apt in attrs:
                if apt[0] == 'data-artist':
                    self.artist = apt[1]
                if apt[0] == 'data-title':
                    self.title = apt[1]

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.title and self.artist:
                self.result.append([self.artist, self.title])
                self.title = ''
                self.artist = ''


class ParseYear(HTMLParser):
    """
    Find the weekly charts for a given year
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = []

    def handle_starttag(self, tag, attrs):
        for apt in attrs:
            if apt[0] == 'href':
                if apt[1].startswith('/charts/hot-100/'):
                    ldata = apt[1].split('/')
                    self.result.append(ldata[-1])


def read_data(url_page, parser):
    """
    Call requests.get for a url and return the extracted data.

    Parameters:
        url_page -- url of the Billboard data
        parser -- Instantiated parser (either ParseWeek() or ParseYear().
    """
    req = requests.get(url_page)
    parser.feed(req.text)
    return parser.result


def get_all_chart_ids():
    """
    Scan Billboard files and return a list.  Each entry in that list
    is a list of week names for a year.  If data for past years does
    not exist, initialize the daata for all past years.  Otherwise,
    just return a list for the current year.
    """
    charts = []
    now = datetime.now()
    yrval = "data%s%d" % (os.sep, START_YEAR)
    try:
        _ = os.listdir(yrval)
        st_year = now.year
    except FileNotFoundError:
        st_year = START_YEAR
    for year in range(st_year, now.year + 1):
        lyear = str(year)
        info = read_data(YEAR_URL % lyear, ParseYear())
        if info[0].endswith('01-08'):
            info.insert(0, '%s-01-01' % lyear)
        if info[0] == '2018-01-03':
            info = info[1:]
        charts.append(info)
    return charts


def main():
    """
    Extract the data from the Billboard Hot-100 charts into a local
    directory.  First make sure that the year subdirectory exists,
    and for every week of that year (info extracted from get_all_chart_ids)
    generate a list of artists and titles.  Save that list as an
    appropriately named json file.
    """
    info = get_all_chart_ids()
    for year in info:
        year_dir = year[0].split('-')[0]
        year_path = "%s%s%s" % ('data', os.sep, year_dir)
        try:
            os.listdir(year_path)
        except FileNotFoundError:
            os.mkdir(year_path)
        print(year_path)
        for week in year:
            winfo = read_data(WEEK_URL % week, ParseWeek())
            ofname = "%s%s%s" % (year_path, os.sep, week)
            with open(ofname, 'w', encoding='utf8') as outfile:
                json.dump(winfo, outfile, ensure_ascii=False)
            print(week)


if __name__ == '__main__':
    main()
