#!/usr/bin/python
# pylint: disable=W0223
"""
Concordance routines.  Search for words in titles of Billboaard Hot-100
songs.
"""
import codecs
import re
import sys
import operator
from scanner import Scanner

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
REGEXA = re.compile('[^a-z ]')
TRANSTAB = str.maketrans('/', ' ')
FIRST_DATE = 'first-date'
LAST_DATE = 'last-date'
WEEKS_ON = 'weeks-on'
BEST = 'best'


class ConcScan(Scanner):
    """
    Local scanner used by the concordance program.

    self.paramv is the word to be scanned (magicw).
    """
    def __init__(self, magicw):
        Scanner.__init__(self, magicw)
        self.song_list = []
        self.answer = [[], []]

    def sfunc(self, entry, week_name, count):
        if self.paramv:
            tvalue = find_word(self.paramv, entry[1])
            if tvalue >= 0:
                self.answer[tvalue].append([entry, week_name, count])
        self.song_list.append(entry[1])


def organize_answer(answer):
    """
    Organize a list of entries into a unified dictionary.

    Input parameter:
        answer -- list of entries.  Each entry represents a song's
                  appearance on the chart and consists of a list that
                  includes, the song's title and artist (inside another
                  list), the date of the entry, and the position on the
                  charts.

    Ouput:
        A dictionary indexed by song title.  The value of each entry
        is a dictionary indexed by artist.  The contents of entries in
        that dictionary is a dictionary of the first date that the song
        appears on the charts, the last date that the song appears on
        the charts, the total number of weeks that the song appears
        on the charts, and the peak postion of that song.
    """
    retdict = {}
    for entry in answer:
        rank = entry[2] + 1
        datev = entry[1].split('/')[-1]
        if entry[0][1] not in retdict:
            retdict[entry[0][1]] = {}
        localp = retdict[entry[0][1]]
        if entry[0][0] not in localp:
            newperf = {}
            newperf[FIRST_DATE] = datev
            newperf[LAST_DATE] = datev
            newperf[WEEKS_ON] = 1
            newperf[BEST] = rank
            localp[entry[0][0]] = newperf
        else:
            localp[entry[0][0]][LAST_DATE] = datev
            localp[entry[0][0]][WEEKS_ON] += 1
            if rank < localp[entry[0][0]][BEST]:
                localp[entry[0][0]][BEST] = rank
    return retdict


def find_word(word, song):
    """
    Input:
       word -- word being scanned for
       song -- song title

    Return:
       -1 if word is not in song.
       0 if word is in song.
       1 if word in in text of the song ('train' contains 'rain')
    """
    titlew = REGEXA.sub('', song.lower().translate(TRANSTAB))
    if titlew.find(word) < 0:
        return -1
    if titlew == word:
        return 0
    if titlew.startswith(word + ' '):
        return 0
    if titlew.endswith(' ' + word):
        return 0
    if titlew.find(' ' + word + ' ') > 0:
        return 0
    return 1


def check_conc(magic_word=''):
    """
    Accumlate a list of song titles from the information in the data
    directory.

    If magic_word is false, then generate a concordance of the words in
    the song lyrics

    If magic_word is a word value, return a structure of information
    about songs with that word in the title
    """
    magic_word = magic_word.lower()
    chk_conc_scan = ConcScan(magic_word)
    chk_conc_scan.do_scan()
    if magic_word:
        return (organize_answer(chk_conc_scan.answer[0]),
                organize_answer(chk_conc_scan.answer[1]))
    return gen_concordance(chk_conc_scan.song_list)


def gen_concordance(song_list):
    """
    Generate a concordance of words in song titles.

    Parameters:
        song_list -- list of song titles

    Returns:
        A structure whose entries are indexed by words.  The value of each
        entry is the number of times that word appears in song titles.
    """
    final_list = list(set(song_list))
    concordance = {}
    for song in final_list:
        for word in song.split(' '):
            windx = word.lower()
            indx = ''
            for charcter in windx:
                if charcter in 'abcdefghijklmnopqrstuvwxyz':
                    indx += charcter
            if indx in concordance:
                concordance[indx] += 1
            else:
                concordance[indx] = 1
    sorted_info = sorted(concordance.items(), key=operator.itemgetter(1))
    return sorted_info


if __name__ == '__main__':
    print(check_conc('breakfast'))
    print(check_conc('chameleon'))
    print(check_conc(''))
