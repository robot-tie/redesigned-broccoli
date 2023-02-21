#################################
#   Author: Raymond Dillon      #
#   Email:  ray@raytheitguy.com #
#################################

from bs4 import BeautifulSoup
import requests
import time
import argparse

parsedargs = argparse.ArgumentParser()
#create argument parameters and assign to variables
parsedargs.add_argument('-u',   '--url',      help = "If you only wish to examine one URL, use this followed by the url. Include http/https.")
parsedargs.add_argument('-f',   '--file',     help = "If you have a txt file with domains on separate lines use this. Ensure they have protocol: http/https.")
parsedargs.add_argument('-t',   '--delay',    help = "If you are sending a request using your txt file, you may wish to include a time delay in seconds.")
parsedargs.add_argument('-o',   '--output',   help = "Enter the name file you wish to have the results saved in.")
parsedargs.add_argument('-t1',  '--tag1',     help = "Enter the name of the html tag you are most interested in finding.")

#collect argument values and assign to their local variable
args    = parsedargs.parse_args()
url     = args.url
file    = args.file
delay   = args.delay
output  = args.output
tag1    = args.tag1

#check to see if there is a url or file passed
def checkparams(url, file):
    #check the value of url and file
    if (url is None and file is None) or (tag1 is None):
        print("No value detected for either -u (single URL), -f (txt file with URLs) or -tag1 (html tag name). Exiting.")
        SystemExit(1)
    else:
        pass


#create the request variable
#set headers to send with get request
HEADERS1 = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36'),
                          'referer': 'https://google.com/'}
#add new headers to cycle through
"""
HEADERS2 = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36'),
                          'referer': 'https://google.com/'}

HEADERS3 = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36'),
                          'referer': 'https://google.com/'}

HEADERS4 = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36'),
                          'referer': 'https://google.com/'}
"""
#print(HEADERS)
def getUrls(path):




#open up and read the contents of the txt file that contains the urls
with open(myurls, "r") as fp:
    for url in fp:
        #select the url from the text file trimming off the newline character at the edn
        selection = url[:len(url)-1]
        #send a request using selection and assign the result to a variable called result
        result = requests.get(selection, HEADERS1)
        #create a file with the selection content and name it "selection".html
        filename = selection.replace("://", "")
        filename = filename.replace(".", "")
        f = open(filename+".html", "w")
        f.write(selection)
        f.write(result.text)
        f.close()
#assign a the file that has been retrieved to the variable myfile
#myfile =
#with open(myfile, r) as fp:
#    soup = BeautifulSoup(fp, "html.parser")
