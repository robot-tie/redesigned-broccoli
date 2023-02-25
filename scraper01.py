#################################
#   Author: Robot-Tie           #
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
parsedargs.add_argument('-w',   '--wordlist', help = "Supply a wordlist if you would like to search for files/foldes appended to the domain.")
#parsedargs.add_argument('-s',   '--specfile', help = "Enter the name of the html tag you are most interested in finding.")

#collect argument values and assign to their local variable
args        = parsedargs.parse_args()
url         = args.url
file        = args.file
delay       = args.delay
output      = args.output
tag1        = args.tag1
wlist       = args.wordlist
#sfile       = args.specfile
#variables
founddir    = "200s.txt"
others      = "others.txt"
#check to see if there is a url or file and html tag passed
def checkparams(url, file, tag1):
    #check the value of url and file
    if (url is None and file is None) or (tag1 is None):
        print("No value detected for either -u (single URL), -f (txt file with URLs) or -tag1 (html tag name). Exiting.")
        SystemExit(1)
    else:
        pass
#file finder function
def filefinder(url):
    print("Received from get request: ", url)
    n = open(others, "a")
    ffiles = ""
    with open(wlist) as wl:
        for item in wl:
            cleanitem = item.replace("\n", "")
            newurl = url + "/" + cleanitem
            #getrequestd(cleanitem)
            dirs = requests.get(newurl)
            print(newurl)
            print(dirs.status_code)
            if dirs.status_code == 200:
                ffiles += newurl
                ffiles += "\n"
                #founddir(newurl)
                print("FOUND")
            time.sleep(2)
        return ffiles

#create a function to send a request to a single URL
def getrequest(url):
    #delete next line after testing
    print("Requesting: ", url)
    #send a request and save it in myrequest
    try:
        #create a file name removing any special characters
        resultsfile = url.replace(".", "")
        resultsfile = resultsfile.replace(":", "")
        resultsfile = resultsfile.replace("/", "")
        resultsfile = resultsfile + ".html"
        #send the get request and assign it to myrequest
        myrequest = requests.get(url, HEADERS1)
        #check the server response code
        if (myrequest.status_code == 200):
            #if a wordlist is supplied run it
            if wlist:
                dir = filefinder(url)
                d = open(founddir, "a")
                d.write(dir)
                d.write("\n")
                d.close()
            f = open(resultsfile, "w")
            f.write(url)
            f.write(myrequest.text)
            f.close()
            #make a request to parse the html tags
            print("Sending to parser..")
            parsehtml(resultsfile)
            
        elif (myrequest.status_code == 500):
            print("Server error code: ", myrequest.status_code)
        #handle other status codes
        else:
            print(myrequest.status_code)
            print(myrequest.headers)
            print(myrequest.text)
    except:
        print("Error during send request for URL: ", url)

#function to search html files for tags and attributes
def parsehtml(htmlfile):
    print("Made it to html parser!")
    with open(htmlfile, "r") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        links = soup.find_all(tag1)
        #check if links has data
        if links:
            print("Links is good in html parser.")
            #create a new file name to contain results after parsing html
            parsedresults = htmlfile.replace(".", "")
            parsedresults = parsedresults + ".csv"
            fname = open(parsedresults, "w")
            print("After opening file parsedresults")
            fname.write("Results from file: " + htmlfile + "\n")
            for each_tag in links:
                print("Entered loop in parser")
                #write the results to the new file
                fname.write(str(each_tag) + "\n")
                #delete next line after completion
                print(each_tag)
            fp.close()
            fname.close()
        else:
            print("That tag doesn't exist in: ", htmlfile)


#check to see if we will be scanning for a single URL or a file or URLs
def validurl(url):
    http    = url[:4]
    https   = url[:5]
    #if the url is valid call the single URL scanner
    if url:
        if (https == 'https'):
            #delete next line after testing
            #print("Protocol detected is: ", https)
            return True
        elif (http == 'http'):
            #delete next line after testing
            #print("Protocol detected is: ", http)
            return True
        else:
            #print("Please check your protocol is included and correct: http/https. Exiting.")
            return False
    else:
        print("No valid url detected during validurl() check. Exiting.")
        SystemExit(1)

#function to call for one url submitted
def oneurl(url):
    #send it to the valid url checker
    if validurl(url):
        #send it to get a request
        getrequest(url)
    else:
        print("URL not valid. Exiting.")
        SystemExit(1)

#check if a file submitted is correctly formatted and if so make the request, if not let the user know which item will not work
def validfile(file):
    #try to open the file to make sure it is valid
    try:
        with open(file, "r") as fp:
            #look through the items
            for item in fp:
            #clean the url of new line characters and white spaces
                cleanurl = item.replace("\n", "")
                cleanurl = cleanurl.replace(" ", "")
                #send the url to be checked for protocol
                if validurl(cleanurl):
                    #if the return value is true send it getrequest
                    #print("URL: ", cleanurl, " is valid.")
                    getrequest(cleanurl)
                #if it isn't valid, let the user know which URL isn't valid
                else:
                    print("Please check your file for URL: ", cleanurl, " as it appears to not be valid.")
                time.sleep(2)
    except:
        print("File not found. Please check your path and file name. Exiting.")
        SystemExit(1)
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
"""
#open up and read the contents of the txt file that contains the urls
with open(url, "r") as fp:
    for myurl in fp:
        #select the url from the text file trimming off the newline character at the edn
        selection = myurl[:len(myurl)-1]
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
"""
def getstarted():
    checkparams(url, file, tag1)
    if url:
        #do something
        oneurl(url)
    elif file:
        #do something else
        validfile(file)
    else:
        print("No file or url detected in getstarted() function. Exiting.")
        SystemExit(1)

getstarted()