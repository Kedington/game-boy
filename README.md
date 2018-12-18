# game-boy

Inspired by the game Gameboy from the podcast [If I Were You](https://headgum.com/if-i-were-you)<br>
This app goes through all of your emails looking for words that only appear in one email

### Instalation 
After cloning follow the insturctions in the [Python QuickStart Guide](https://developers.google.com/gmail/api/quickstart/python) 
You will need to set up a credentials.json and install the google client library

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
