#!/usr/bin/python
# pylint: disable=W0223
"""
Produce html files containg song info with specific words in their titles.
"""
import os
import yaml
from concordance import check_conc


def wrap(headr, data):
    """
    Input:
       headr -- text of html field
       data -- text to be wrapped.

    Returns a corresponding portion of an html file.
    """
    return '<%s>%s</%s>' % (headr, data, headr)


def fmt_table(tbl_info):
    """
    Format a table.  tbl_info is a list of lists.  Each list in tbl_info
    is a line of fields.  Wrap the fields in td html blocks and the lines
    in tr html blocks
    """
    output = []
    for tline in tbl_info:
        local_line = ''
        for field in tline:
            local_line += wrap('td', field)
        output.append(wrap('tr', local_line))
    return '\n'.join(output)


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
            record.append(info['first-date'])
            record.append(info['last-date'])
            record.append(str(info['weeks-on']))
            record.append(str(info['best']))
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
    with open("template.txt", 'r') as inputstr:
        template = inputstr.read()
    for word in config_data['words']:
        table_data = fmt_table(gen_table(check_conc(word)))
        ofilen = config_data['directory'] + os.sep + word.lower() + '.html'
        with open(ofilen, 'w') as ofile:
            ofile.write(template % word)
            ofile.write(table_data)
            ofile.write('</table></div></body></html>\n')


if __name__ == '__main__':
    main()
