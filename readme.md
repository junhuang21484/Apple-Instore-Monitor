# Apple In-Store Monitor

A lightweight, multi-threaded Python monitor for checking nearby Apple Store pickup availability. Configure one or more product IDs, choose a ZIP code, and receive notifications when a product becomes available for pickup.

> [!IMPORTANT]
> This public version **does not include cookie generation or automatic cookie renewal**. Apple may reject fulfillment requests with status code `541` when a valid session cookie is required.
>
> A separate, fully automated version that generates and refreshes the required cookies is available, but it is not included in this repository.

## Features

- Monitors multiple Apple product IDs concurrently
- Searches stores near a configured ZIP code
- Supports Discord webhook and Windows desktop notifications
- Allows specific stores to be excluded from notifications
- Supports authenticated and unauthenticated HTTP proxies
- Rotates proxies in thread-safe round-robin order
- Uses configurable monitor, error, and task startup delays

## How it works

Each configured product runs in its own monitoring thread:

1. The monitor requests pickup availability from Apple's fulfillment endpoint.
2. The response is parsed into structured store-availability records.
3. Available products are sent to the enabled notification services.
4. When proxies are enabled, a failed request moves that task to the next proxy.
5. The task waits for the configured delay and checks again.

## Requirements

- Python 3.9 or newer
- Windows for native desktop notifications
- A Discord webhook if Discord notifications are enabled
- Optional HTTP proxies

## Installation

1. Download or clone the repository.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Configure `data/monitor_data.json` and, if needed, `data/proxies.txt`.
6. Start the monitor:

   ```powershell
   python main.py
   ```

## Configuration

The monitor is configured through `data/monitor_data.json`:

```json
{
  "product_list": {
    "PRODUCT_ID": "Product display name"
  },
  "monitor": {
    "delay": {
      "error_delay": 60,
      "monitor_delay": 8,
      "load_up_delay": 2
    },
    "near_zip": "10001",
    "use_proxy": false
  },
  "notifications": {
    "exclude_store_list": [
      "Store name to ignore"
    ],
    "discord": {
      "on": false,
      "webhook": "YOUR_DISCORD_WEBHOOK",
      "mention_all": false
    },
    "desktop": {
      "on": false
    }
  }
}
```

### Products

`product_list` maps each Apple part number to the name shown in logs and notifications:

```json
{
  "PRODUCT_ID": "Product display name"
}
```

You may add multiple entries. Each entry starts a separate monitoring task.

### Monitor settings

| Setting | Description |
| --- | --- |
| `error_delay` | Seconds to wait after an error when proxies are disabled |
| `monitor_delay` | Seconds between availability checks for each task |
| `load_up_delay` | Seconds between starting product-monitor threads |
| `near_zip` | ZIP code used to locate nearby Apple Stores |
| `use_proxy` | Enables or disables proxy rotation |

Use reasonable delays. Very frequent requests can cause throttling or temporary rejection.

### Notifications

Discord notifications require a webhook URL. Set `mention_all` to `true` to include `@everyone` in availability alerts.

Desktop notifications use the local Windows notification system. Both notification methods can be enabled simultaneously.

Store names listed in `exclude_store_list` are removed before notifications are sent.

## Proxies

Add one proxy per line to `data/proxies.txt`. The following formats are supported:

```text
HOST:PORT
HOST:PORT:USERNAME:PASSWORD
```

The shared proxy service distributes proxies in round-robin order. Selection is protected by a lock, so concurrent product threads cannot corrupt the rotation index. A proxy can still be assigned to more than one task after the list wraps around.

If `use_proxy` is `true`, at least one valid proxy must be present.


### No availability is reported

- Confirm the Apple product ID.
- Verify the ZIP code.
- Check the response status in the console.
- Remember that unavailable products do not trigger notifications.


## Roadmap

- Product ID lookup
- Richer Discord notifications with product links
- Optional notification sounds
- Additional configuration validation

## Notification example

![Discord availability notification example](https://media.discordapp.net/attachments/895816713554235513/896186072613138502/unknown.png)

## License

This project is available under the [MIT License](LICENSE).
