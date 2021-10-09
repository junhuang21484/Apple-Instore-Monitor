# Welcome to Apple In-store Monitor

This is a monitor that are not fully scaled, and might still have some bugs. You can edit
```monitor_data.json``` file to edit what product this monitor will monitor, and which store you want to monitor.

### Monitor Data - Product List
```
A dictonary in the formatted in {"product id": "product name"}, you will need to set the product
name manually, and this is what it will show up in your discord webhook.

You can add your own product, as long as you have the product id.
```

### Monitor Data - Setting
```
Delay - The time the monitor will wait inside each thread for each product
Item cooldown - The time where an item and store will get removed from the cooldown list
Webhook - The webhook url of your discord, the bot will send notifications to this url
Store near - The store id where you want to monitor. It will also monitor nearby stores
Notification Settings:
- Desktop (True if you want to get desktop notifications)
- Sound (True if you want to get sound notifications) [Currently not supported]
```

### Installation
```
1. Download the code from the repo
2. In CMD run pip install -r requirements.txt to install all the requirements
3. Configure monitor_data.json to your need (You must add a webhook url, and change the store 
to one near you)
4. Run main.py to start monitoring
```

### To be added
```
1. Store id searching via Zip Code/Store Name
2. Product ID auto look up
3. Better discord notification with auto item url etc.
4. Sound notifications for Windows
5. Desktop notifications for Windows
6. More flexible control over monitor_data.json
```

### Discord Notification Example
![This is a picture of discord notification example](https://media.discordapp.net/attachments/895816713554235513/896186072613138502/unknown.png)
