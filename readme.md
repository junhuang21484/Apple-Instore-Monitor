# Welcome to Apple In-store Monitor

This is a monitor that are not fully scaled, and might still have some bugs. You can edit
```monitor_data.json``` file to edit what product this monitor will monitor, and which store you want to monitor.
The monitor can monitor multiple products at the same time, but can only monitor one store and its nearby store at
once.

**Monitor Data - Product List**
```
A dictonary in the formatted in {"product id": "product name"}, you will need to set the product
name manually, and this is what it will show up in your discord webhook.

You can add your own product, as long as you have the product id.
```

**Monitor Data - Setting**
```
Delay - The time the monitor will wait inside each thread for each product
Webhook - The webhook url of your discord, the bot will send notifications to this url
Store near - The store id where you want to monitor. It will also monitor nearby stores
```

##Discord Notification Example
![This is a picture of discord notification example]()
