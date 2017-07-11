from amcrest import AmcrestCamera as _AmcrestCamera

from thief_snapshot.cameras.base import BaseCamera


class AmcrestCamera(BaseCamera):
    def __init__(self, *args, **kwargs):
        super(AmcrestCamera, self).__init__(*args, **kwargs)
        self.camera = _AmcrestCamera(
            self.ip,
            self.port,
            self.username,
            self.password,
        ).camera

    def snapshot(self):
        """Takes a snapshot with the camera.

        Returns:
            file object
        """
        return self.camera.snapshot(0)
