# game-boy

Inspired by the game <i>Gameboy</i> from the podcast <i>[If I Were You](https://headgum.com/if-i-were-you)</i>.
  
The goal of Gameboy is to think of a word that only appears in one of your emails.<br>
This script finds all possible solutions by going through your emails and keeping track of words that only appear once.

### Instalation 
After cloning follow the insturctions in the [Python QuickStart Guide](https://developers.google.com/gmail/api/quickstart/python).<br>
You will need to set up a credentials.json and install the google client library.

### Running 
```
python3 GameBoy.py
```

### Output 
A List of words that appear in only one email
```
{'jake', 'and', 'amir', 'have', 'the', 'best', 'podcast'}
```

### Performance 
Using the Gmail Api a seperate [request](https://developers.google.com/gmail/api/v1/reference/users/messages/get) 
is needed for each email this leads to very slow performance. <br>
When using please be mindful of the [API Usage Limits](https://developers.google.com/gmail/api/v1/reference/quota) 
