"""Module containing base presence detector object that other presence
detector classes inherit from."""


class BasePresenceDetector(object):
    def __init__(self, ip, port, username, password, expected_macs):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.expected_macs = expected_macs

    @property
    def is_presence_detected(self):
        """Checks whether the expected device is online.

        Returns:
            boolean -- whether the expected device was detected
        """
        raise NotImplementedError()
