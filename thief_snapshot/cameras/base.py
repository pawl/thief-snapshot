"""Module containing base camera object that other cameras inherit from."""


class BaseCamera(object):
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def snapshot(self):
        """Takes a snapshot with the camera.

        Returns:
            file object
        """
        raise NotImplementedError()

    @property
    def is_motion_detected(self):
        """Indicates whether motion is detected from the camera.

        Returns:
            boolean -- whether the expected MAC address was detected
        """
        raise NotImplementedError()
