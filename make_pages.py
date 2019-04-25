#!/usr/bin/python
# pylint: disable=W0223
"""
Produce html files containg song info with specific words in their titles.
"""
import os
import yaml
from htmlutil import fmt_table
from htmlutil import OutputInterface
from concordance import check_conc
from concordance import FIRST_DATE
from concordance import LAST_DATE
from concordance import WEEKS_ON
from concordance import BEST


WORDTABLE_HEADER = "Billboard Hot-100 Songs containing the word %s"


def gen_table(conc_data):
    """
    Input:
        conc_data -- data returned from a concordance check_conc call.

    Rearrange the data in the dictionary data from conc_data into rows
    appropriate for a table.  Output is a list of lines, where each
    line is a list of field values.
    """
    out_info = []
    for title in conc_data:
        for cnt, artist in enumerate(conc_data[title]):
            record = []
            if cnt == 0:
                record.append(title)
            else:
                record.append('')
            record.append(artist)
            info = conc_data[title][artist]
            record.append(info[FIRST_DATE])
            record.append(info[LAST_DATE])
            record.append(str(info[WEEKS_ON]))
            record.append(str(info[BEST]))
            out_info.append(record)
    return out_info


def main():
    """
    Read page_data.yaml which contains a list of words to be checked.
    When this program finishes, song titles containing these words and
    information about the song will be displayed in html files saved
    in whatever directory indicated by the directory variable also
    extracted from page_data.yaml

    template.txt is a template for most of the html file.

    This routine loops through the word list and produces the files.
    """
    with open("page_data.yaml", 'r') as inputstr:
        config_data = yaml.safe_load(inputstr)
    ointf = OutputInterface('template.txt')
    for word in config_data['words']:
        table_info = check_conc(word)
        for enumv, hdr in enumerate(['', 'rejects_']):
            table_data = fmt_table(gen_table(table_info[enumv]))
            ofilen = config_data['directory'] + os.sep
            ofilen += hdr + word.lower() + '.html'
            title = WORDTABLE_HEADER % word
            header = ['Song', 'Artist', 'First Date', 'Last Date',
                      'No. of Weeks', 'Peak']
            ointf.build_page(ofilen, title, header, table_data)
            ointf.output()


if __name__ == '__main__':
    main()
