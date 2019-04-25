#!/usr/bin/python
# pylint: disable=W0223
"""
Class used to iterate through all the data saved in json files.
"""
from datetime import datetime
import os
import json
from scanbillboard import START_YEAR


class Scanner(object):
    """
    Scanner is an encapsulation of a scan routine which can be used by
    children of this object. __init__ and sfunc are intended to be
    overridden.
    """
    def __init__(self, param):
        self.paramv = param

    def do_scan(self):
        """
        Iterate through all the json files.  Calls sfunc at the
        deepest point.
        """
        now = datetime.now()
        year_lim = now.year + 1
        for year in range(START_YEAR, year_lim):
            year_dir = 'data%s%d' % (os.sep, year)
            topdir = os.listdir(year_dir)
            for week in topdir:
                week_name = '%s%s%s' % (year_dir, os.sep, week)
                with open(week_name, encoding='utf-8') as fname:
                    song_data = json.load(fname)
                    for count, entry in enumerate(song_data):
                        self.sfunc(entry, week_name, count)

    def sfunc(self, entry, week_name, count):
        """
        Local function

        Gets passed song and artist info as entry.  Week_name is
        the date of this week's chart, and count is how high up
        this work is on the chart.

        This method is intended to get overridden by functions
        implementing uses of this object.
        """
        return [entry, week_name, count, self.paramv]
