from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from time import sleep
from pprint import pprint 
from base64 import b64decode
from collections import defaultdict

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

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
    words = defaultdict(int)

	# Loop through while the nextPageToken is not in the msg_list
    while 'nextPageToken' in msg_list:
        counter += 1
        message_ids = msg_list['messages']
        for message_node in message_ids:
            message_id = message_node['id'] 
            message = service.users().messages().get(userId='me', id=message_id, fields='payload(headers, parts/body/data)').execute()

            # Extract Subject and Body 
            subject = [header['value'] for header in message['payload']['headers'] if header['name'] == 'Subject'][0]
            print(subject)
            if 'parts' in message['payload']:
                body_raw = message['payload']['parts'][0]['body']['data'].replace("-", "+").replace("_", "/")
                body = b64decode(body_raw).decode('utf-8')
                unique_words = ''.join(filter(lambda x: x.isalpha() or x.isspace(), body)).lower().split()
                for word in unique_words:
                    if len(word) < 15:
                        words[word] += 1
        pprint(words)
        print(len(words))
        break
        page_token = msg_list['nextPageToken']
        
        sleep(1) # Sleep For a second as to no exceed quota units 
        msg_list = service.users().messages().list(userId='me', pageToken=page_token).execute()
        


if __name__ == '__main__':
    main()
