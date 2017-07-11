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
