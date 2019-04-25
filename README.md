# Billboard Hot-100 Analysis 

Locally, this repo makes use of a data directory where all the Hot-100
information will be stored.

## scanbillboard.py

Screen scraper for Billboard Hot-100.  If the data/1958 (first year)
directory does not exist, running the main routine from this module
will scrape data for all the years (1958 to current).  If it does
exist, only the current year will be scraped (good for updating the
data every week).

## concordance.py

check_conc is the main routine in this module.  If passed a False value,
(typically ''), then a dictionary is returned containing song title words
and the number of times that they appear in songs.  If a word is passed,
then a structure is returned containing data about songs where that word
appears in the title.

## make_pages.py

Repeatedly run the check_conc program for different words.  Produce an
html page of the results for each word.  Page_data.yaml is a file that
contains the list of words and the directory where the html pages will
be stored.
 
## common_names.py

Find the names of songs that match artists.  Currently just prints out
the information on exact matches.

## scanner.py

Class used locally that loops through all the data.  sfunc and __init__
are  implemented by classes that inherit this class in order to perform
desired  actions.

## htmlutil.py

Collection of routines used for formatting html pages.

