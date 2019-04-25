#!/usr/bin/python
# pylint: disable=W0223
"""
Look for matches between song titles and artist names.
"""
import codecs
import sys
import os
from datetime import datetime
import yaml
from scanner import Scanner
from htmlutil import OutputInterface
from htmlutil import fmt_table

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class PrintScan(Scanner):
    """
    self.artists is a list of artists
    self.songs is a list of song titles
    self.all_data is a list of all records for every week.
    """
    def __init__(self):
        super(PrintScan, self).__init__(self)
        self.artists = []
        self.songs = []
        self.all_data = []

    def sfunc(self, entry, week_name, count):
        self.artists.append(entry[0])
        self.songs.append(entry[1])
        self.all_data.append([entry[0], entry[1], week_name, count])


def get_song_artist_matches():
    """
    Loop through all the saved data and find exact matches between
    song titles and performers.  Return the result as a list of lists,
    each internal list representing a line.
    """
    chk_conc_scan = PrintScan()
    chk_conc_scan.do_scan()
    resulta = list(set(chk_conc_scan.artists))
    results = list(set(chk_conc_scan.songs))
    answers = {}
    for entry in resulta:
        if entry in results:
            answers[entry] = [[], []]
            for info in chk_conc_scan.all_data:
                if entry == info[0]:
                    answers[entry][0].append(info)
                if entry == info[1]:
                    answers[entry][1].append(info)
    structv = {}
    for dupval in answers:
        structv[dupval] = []
        for entry in answers[dupval]:
            best = 100
            record = []
            for week in entry:
                if week[3] < best:
                    record = week
                    best = week[3]
            structv[dupval].append(record)
    return output_info(structv)


def output_info(structv):
    """
    Display info compiled into structv
    """
    count = 0
    retv = []
    for keyv in sorted(structv):
        if structv[keyv][0][0] == structv[keyv][0][1]:
            continue
        if structv[keyv][1][0] == structv[keyv][1][1]:
            continue
        table_line = []
        count += 1
        table_line.append("%d" % count)
        table_line.extend(out_line(structv[keyv][1]))
        table_line.extend(out_line(structv[keyv][0])[1:])
        retv.append(table_line)
    return retv


def out_line(song_info):
    """
    Concatenate all the info into a line on the table
    """
    datev = fix_date(song_info[2])
    retv = [song_info[0], str(song_info[3] + 1), datev, song_info[1]]
    return retv


def fix_date(oldfmt):
    """
    Convert .../YYYY-MM-DD to Month Day, Year format
    """
    dval = oldfmt.split('/')[-1]
    datev = datetime.strptime(dval, "%Y-%m-%d")
    return datev.strftime("%B %-d, %Y")


XTRAEDIT = [['.green { background-color: rgba(0,255,0,.25); }\n',
             '</style>'],
            ['<colgroup> <col span="4" /> <col class="green" /> </colgroup>\n',
             '<tr>']]


def main():
    """
    Write the common_songs.html file.  Data is extracted by the
    get_song_artist_matches routine.
    """
    with open("page_data.yaml", 'r') as inputstr:
        config_data = yaml.safe_load(inputstr)
    ointf = OutputInterface('template.txt')
    table_data = get_song_artist_matches()
    ofilen = config_data['directory'] + os.sep + 'common_songs.html'
    title = 'Song Titles and Band Name Overlap'
    header = ['No.', 'Artist', 'Peak', 'Date', 'Song/Artist', 'Peak',
              'Date', 'Song']
    ointf.build_page(ofilen, title, header, fmt_table(table_data))
    ointf.inject(XTRAEDIT)
    ointf.output()


if __name__ == '__main__':
    main()
