# Billboard Hot-100 Analysis 

Locally, this repo makes use of a data directory where all the Hot-100
information will be stored.

# scanbillboard.py

Screen scraper for Billboard Hot-100.  If the data/1958 (first year)
directory does not exist, running the main routine from this module
will scrape data for all the years (1958 to current).  If it does
exist, only the current year will be scraped (good for updating the
data every week).

# concordance.py

check_conc is the main routine in this module.  If passed a False value,
(typically ''), then a dictionary is returned containing song title words
and the number of times that they appear in songs.  If a word is passed,
then a structure is returned containing data about songs where that word
appears in the title.

