from amcrest import AmcrestCamera as _AmcrestCamera

from thief_snapshot.motion_detection.base import BaseMotionDetector


class AmcrestCameraMotionDetector(BaseMotionDetector):
    def __init__(self, *args, **kwargs):
        super(AmcrestCameraMotionDetector, self).__init__(*args, **kwargs)
        self.camera = _AmcrestCamera(
            self.ip,
            self.port,
            self.username,
            self.password,
        ).camera

    @property
    def is_motion_detected(self):
        """Indicates whether motion is detected from the camera.

        Returns:
            boolean -- whether the expected MAC address was detected
        """
        return self.camera.is_motion_detected
