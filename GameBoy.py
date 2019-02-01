from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from time import sleep
from pprint import pprint 
from base64 import b64decode
import re

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

# Parses out all non Alphabetic or spaces and returns a list
# of all words in the string 
def parse_string(dirty_string):
    parsed_words = re.sub(r'\s*[^A-Za-z]+\s*', ' ', dirty_string).lower().split()
    return parsed_words.split() 

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail Api to get list of inital 100 message ids
    msg_list = service.users().messages().list(userId='me').execute()
    counter = 0
    msg_counter = 0
    headers = ['Subject']

    words = set()
    gameboy_words = set()

    # Loop through while the nextPageToken is not in the msg_list
    while True:
        counter += 1
        message_ids = msg_list['messages']
        for message_node in message_ids:
            message_id = message_node['id'] 
            message = service.users().messages().get(userId='me', id=message_id, fields='payload(headers, parts/body/data)').execute()

            # Extract Subject from the headers
            subject = [header['value'] for header in message['payload']['headers'] if header['name'] == 'Subject'][0]
            subject_words = re.sub(r'\s*[^A-Za-z]+\s*', ' ', subject).lower().split()
            
            # Extract the Body and Decode it into plane text
            if 'parts' in message['payload']:
                body_raw = message['payload']['parts'][0]['body']['data'].replace("-", "+").replace("_", "/")
                body = b64decode(body_raw).decode('utf-8')
                body_words = re.sub(r'\s*[^A-Za-z]+\s*', ' ', body).lower().split()
                total_words = subject_words + body_words
            else:   
                total_words = body_words

            # Loop through all the words adding them to a set that keeps track of unique words and a set that holds repeated words
            for word in total_words:
                if word not in words:
                    if word not in gameboy_words:
                        gameboy_words.add(word)
                    else:
                        gameboy_words.remove(word)
                        words.add(word)

        # If there is still another page continue to get the next list of emails
        if 'nextPageToken' in msg_list:
            page_token = msg_list['nextPageToken']
            msg_list = service.users().messages().list(userId='me', pageToken=page_token).execute()
        else: # all emails have been read 
            pprint(gameboy_words)
            break

if __name__ == '__main__':
    main()
