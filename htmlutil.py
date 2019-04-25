#!/usr/bin/python
# pylint: disable=W0223
"""
Utilities for formatting html pages
"""


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


def make_header(header):
    """
    header is a list of text fields.

    Return a string representing the html text for a table header.
    """
    retv = ''
    for field in header:
        retv += wrap('th', field)
    return wrap('tr', retv)


class OutputInterface(object):
    """
    Output html file.
    """

    def __init__(self, template):
        self.out_data = ''
        self.filename = ''
        with open(template, 'r') as inputstr:
            self.template = inputstr.read()

    def build_page(self, filename, title, headerl, table_data):
        """
        Construct the html file based on the values of the other
        three parameters.
        """
        header = make_header(headerl)
        self.out_data = self.template % title
        self.out_data += header
        self.out_data += table_data
        self.out_data += '\n</table></div></body></html>\n'
        self.filename = filename

    def output(self):
        """
        This routine writes out the data constructed by build_page.
        """
        with open(self.filename, 'w') as ofile:
            ofile.write(self.out_data)

    def inject(self, edits):
        """
        Add some text into the html data.  Edits is a list of paired entries
        consisting of text to add and text to insert this text in front of.
        """
        for fix_text in edits:
            indx = self.out_data.find(fix_text[1])
            firstp = self.out_data[0:indx]
            secondp = self.out_data[indx:]
            self.out_data = firstp + fix_text[0] + secondp

    def get_template(self):
        """
        Return saved template value
        """
        return self.template
