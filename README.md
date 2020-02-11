# python-appsflyer-server-events-api

Python client implementation for [AppsFlyer Server-to-server events API](https://support.appsflyer.com/hc/en-us/articles/207034486-Server-to-server-events-API#setup)

## Why this project exists

Let's be honest, AppsFlyer server-to-server event API is a [horrible mess of bad design decisions](https://medium.com/@DataGreed/bad-api-design-studying-confusing-appsflyer-server-to-server-api-3c0a2af0b991).

This projects aim to simplify interaction with this API and lessen the chances of shooting yourself in the foot. 

## Usage

Example usage:

```python
import appsflyer
from datetime import datetime

client = AppsFlyerEventApiClient(application_id="id1389752090", developer_key="insert_developer_key")
client.track(
  appsflyer_id="1415211453000-6513894", 
  event_name="af_purchase", 
  idfa="AEBE52E7-03EE-455A-B3C4-E57283966239", 
  event_value=appsflyer.EventValue(revenue=6, content_type="wallets", content_id="15854, quantity=1)
  event_currency="USD",
  eventTime=datetime.datetime(2020, 3, 10, 18, 54, 14),
  device_ip="198.51.100.5"
```

## TODO

- add more documentation on EventValue parameters
- put package on PyPi
