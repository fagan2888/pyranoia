from bs4 import BeautifulSoup
import urllib.request

# Generic Scraping Logic
def eat_soup(bs_object):

    contents = ''
    return contents


# Do the scraping
website_list_file = open('../data/websites.txt', 'r')
for line in website_list_file.readline():
    # Load website at the line
    r = urllib.request.urlopen(line).read()
    soup = BeautifulSoup(r)

