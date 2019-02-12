from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from base64 import b64decode
from pprint import pprint 

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
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

	words = set()
	gameboy_words = set()

	# Loop through while the nextPageToken is not in the msg_list
	while True:
		for message_node in msg_list['messages']:
			message = service.users().messages().get(userId='me', id=message_node['id'], fields='payload(headers, parts/body/data)').execute()

			# Extract Subject from the headers
			subject = [header['value'] for header in message['payload']['headers'] if header['name'] == 'Subject'][0]
			subject_words = parse_string(subject)
			
			# Extract the Body and Decode it into plane text
			if 'parts' in message['payload']:
				body_raw = message['payload']['parts'][0]['body']['data'].replace("-", "+").replace("_", "/")
				body = b64decode(body_raw).decode('utf-8')
				body_words = parse_string(body)
				total_words = subject_words + body_words
			else:	
				total_words = subject_words

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

# Parse out all words that include any non alpha characters  
def parse_string(dirty_string):
	words = []
	valid_word = True
	parsed_word = ''
	for char in dirty_string:
		if char.isspace():
			if valid_word and parsed_word:
				words.append(parsed_word)
			valid_word = True
			parsed_word = ''
		elif char.isalpha():
			parsed_word += char.lower()
		else:
			valid_word = False
	if valid_word and parsed_word:
		words.append(parsed_word)
	return words
			
if __name__ == '__main__':
	main()
