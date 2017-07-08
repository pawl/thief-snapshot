"""This is copied from home-assistant's device_tracker/ddwrt.py."""
import re

import requests

from thief_snapshot.presence_detection.base import BasePresenceDetector


_DDWRT_DATA_REGEX = re.compile(r'\{(\w+)::([^\}]*)\}')
_MAC_REGEX = re.compile(r'(([0-9A-Fa-f]{1,2}\:){5}[0-9A-Fa-f]{1,2})')


def _parse_ddwrt_response(data_str):
    """Parse the DD-WRT data format."""
    return {key: val for key, val in _DDWRT_DATA_REGEX.findall(data_str)}


class DDWRTPresenceDetector(BasePresenceDetector):
    def __init__(self, *args, **kwargs):
        super(DDWRTPresenceDetector, self).__init__(*args, **kwargs)

        if not self.expected_macs:
            raise Exception('expected_macs setting is required for ddwrt')

    @property
    def is_presence_detected(self):
        """Checks a dd-wrt router to see if the expected MAC address is online.

        iOS doesn't accept pings while the screen is off, so we have to use
        this to check the router for activity.

        Returns:
            boolean -- whether the expected MAC address was detected
        """
        url = 'http://{}:{}/Status_Wireless.live.asp'.format(self.ip, self.port)
        response = requests.get(
            url,
            auth=(self.username, self.password),
            timeout=4,
        )
        response.raise_for_status()

        data = _parse_ddwrt_response(response.text)
        if not data:
            raise Exception("No data was returned from the router.")

        active_clients = data.get('active_wireless', None)
        if not active_clients:
            return []

        # The DD-WRT UI uses its own data format and then
        # regex's out values so this is done here too
        # Remove leading and trailing single quotes.
        clean_str = active_clients.strip().strip("'")
        elements = clean_str.split("','")

        active_macs = [item for item in elements if _MAC_REGEX.match(item)]

        mac_found = any(active_mac in self.expected_macs
                        for active_mac in active_macs)

        return mac_found
