# Welcome to Apple In-store Monitor

This is a monitor that are not fully scaled, and might still have some bugs. You can edit
```data/monitor_data.json``` file to edit what product this monitor will monitor, and which store you want to monitor.

### Monitor Data - Product List
A dictionary in the formatted in `{"product id": "product name"}`, you will need to set the product
name manually, and this is what it will display on notifications

You can add your own product, as long as you have the product id.

### Monitor Data - Monitor
This is where you config your delays, whether to use proxies or not, and most importantly your local zip code
```
error_delay - you can ignore this section it is not used at current moment
monitor_delay - how many second(s) each task will wait before it check for stock again
load_up_delay - how many second(s) the monitor will wait before it load the next task when starting
near_zip - The zipcode that the bot will check for stock (It will check all nearby store to that zip)
use_proxy - true/false, see proxies section below
```

### Monitor Data - Notifications
This is where you can choose what type of notifications you want on top of the console print
```
discord
    - on: true/false, toggle if you want discord notification or not
    - webhook: the webhook url for where the notification is going to send to
    - mention_all: true/false, toggle if you want to @everyone or not
desktop
    - on: true/false, toggle if you want desktop notification or not
```

### Proxies
Apple now is more strict on how many request you can send before it start banning you from accessing
their api. You can still access the website and make purchases, but the monitor will not be able to
access the stock data anymore. Therefore, it is best if you use proxies so the monitor can swap to a 
new IP when the current one got banned, and it will not affect your local IP. Currently the monitor only
support user auth proxies. 

### Installation
```
1. Download the code from the repo
2. In CMD run pip install -r requirements.txt to install all the requirements
3. Configure monitor_data.json to your need (You must add a webhook url, and change the store 
to one near you)
4. Run main.py to start monitoring
```

### To be added

1. ~~Store id searching via Zip Code/Store Name~~
2. Product ID auto look up
3. Better discord notification with auto item url etc.
4. Sound notifications for Windows
5. ~~Desktop notifications for Windows~~
6. ~~More flexible control over monitor_data.json~~


### Discord Notification Example
![This is a picture of discord notification example](https://media.discordapp.net/attachments/895816713554235513/896186072613138502/unknown.png)
