from bs4 import BeautifulSoup
import requests
import time
#assign a the file name and location if applicable to a variable
myurls = input("Enter your url text file path:")
#create the request variable
#set headers to send with get request
HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36'),
                          'referer': 'https://moonpay.com/'}
#print(HEADERS)
i = 0
#open up and read the contents of the txt file that contains the urls
with open(myurls, "r") as fp:
    for url in fp:
        #select the url from the text file trimming off the newline character at the edn
        selection = url[:len(url)-1]
        #send a request using selection and assign the result to a variable called result
        result = requests.get(selection, HEADERS)
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
