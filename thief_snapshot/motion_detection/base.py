"""Module containing base object that other motion detectors inherit from."""


class BaseMotionDetector(object):
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    @property
    def is_motion_detected(self):
        """Indicates whether motion is detected.

        Returns:
            boolean -- whether the expected MAC address was detected
        """
        raise NotImplementedError()
