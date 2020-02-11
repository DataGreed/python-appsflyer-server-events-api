import logging
import requests
import json
from datetime import datetime
"""
@author Alexey "DataGreed" Strelkov
"""


class EventValue:

    def __init__(self, revenue, content_type, content_id, quantity=None):

        self.revenue = revenue
        self.content_type = content_type
        self.content_id = content_id
        self.quantity = quantity    # seems like it;s optional, docs don't specify

    def as_dict(self):

        result = {
            "af_revenue": str(self.revenue),
            "af_content_type": str(self.content_type),
            "af_content_id": str(self.content_id),
        }

        if self.quantity:
            result["af_quantity"] = str(self.quantity)

    def render(self):
        return json.dumps(self.as_dict())


class AppsFlyerEventApiClient:

    def __init__(self, application_id, developer_key):
        """
        :param application_id:
        :param developer_key:
        See https://support.appsflyer.com/hc/en-us/articles/207034486-Server-to-server-events-API#setup for more info
        """
        self.application_id = application_id
        self.developer_key = developer_key

        try:
            int(application_id)
            logging.warning(f"AppsFlyer: if you're trying to send events for iOS app, your application_id should "
                            f"be id{application_id}, not {application_id} - appsflyer will still return response 200, "
                            f"but will fail silently")
        except ValueError:
            pass

    def get_api_url(self):
        return f"https://api2.appsflyer.com/inappevent/{self.application_id}"

    def track(self, appsflyer_id, event_name, idfa=None, advertising_id=None, device_ip=None, customer_user_id=None,
                 event_time=None, event_value=None, event_currency=None):
        """
        Track server-to-server event to AppsFlyer.
        See https://support.appsflyer.com/hc/en-us/articles/207034486-Server-to-server-events-API#setup for more info
        :param appsflyer_id: Attributes the event to a media source and campaign. Get it from your app.
        :param event_name:
        :param idfa: Parameter is mandatory in order to send in-app event postbacks to external partners.
        :param advertising_id:  Parameter is mandatory in order to send in-app event postbacks to external partners.
        :param device_ip: IP address (ip) is the mobile device’s IP (during an event occurrence).
        IP address determines the event country. If no IP address is specified, the country field shows N/A in the raw data.
        :param customer_user_id: Customer user ID is used to associate in-app events with users in BI systems.
        :param event_time: You can use the optional eventTime parameter to specify the time of the event occurrence
        (in UTC +0 timezone). If the parameter is not included in the message,
        AppsFlyer uses the timestamp from the HTTPS message received.
        :param event_value: A dict containing a rich in-app event value (see the appsflyer docs for keys)
        :param event_currency: currency of an event
        :return: response object (requests library)
        """

        payload = {
            "appsflyer_id": appsflyer_id,
            "eventName": event_name,
            "eventValue": "",   # must be empty string if not set according to docs
            "af_events_api": "true"
        }

        if advertising_id:
            payload["advertising_id"] = advertising_id

        if customer_user_id:
            payload["customer_user_id"] = customer_user_id

        if idfa:
            payload["idfa"] = idfa

        if device_ip:
            payload["ip"]: device_ip

        if event_currency:
            payload["eventCurrency"]: event_currency

        if event_time:
            if isinstance(event_time, str):
                payload["eventTime"]: event_time
            elif isinstance(event_time, datetime):
                payload["eventTime"]: event_time.isoformat(sep=" ")  # TODO: do we need to trim milliseconds to thee positions after point?

        if event_value:
            if isinstance(event_value, str):
                payload["eventValue"] = event_value

            if isinstance(event_value, dict):
                # stringify as docs say
                payload["eventValue"] = json.dumps(event_value)

            #         "eventValue":
            # 	"{
            # 		\"af_revenue\": \"6\",
            # 		\"af_content_type\": \"wallets\",
            # 		\"af_content_id\": \"15854\",
            # 		\"af_quantity\" :\"1\"
            #    }",

        headers = {
            "authentication": self.developer_key,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.get_api_url(), headers=headers, json=payload)

        logging.debug(f"Got AppsFlyer Response: <{response.status_code}> {response.text}")

        return response
