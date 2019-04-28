#!/usr/bin/python
# pylint: disable=W0223
"""
Read all the stored data
"""
import codecs
import sys
from scanner import Scanner

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class SongScan(Scanner):
    """
    self.artists is a list of artists
    self.songs is a list of song titles
    self.all_data is a list of all records for every week.
    """
    def __init__(self):
        super(SongScan, self).__init__(self)
        self.artists = []
        self.songs = []
        self.all_data = []

    def sfunc(self, entry, week_name, count):
        self.artists.append(entry[0])
        self.songs.append(entry[1])
        self.all_data.append([entry[0], entry[1], week_name, count])


def get_song_artist():
    """
    Extract all the information and return as a list of artists, a list
    of songs, and a list of records relating songs to artists.
    """
    chk_conc_scan = SongScan()
    chk_conc_scan.do_scan()
    resulta = list(set(chk_conc_scan.artists))
    results = list(set(chk_conc_scan.songs))
    all_data = chk_conc_scan.all_data
    return resulta, results, all_data
