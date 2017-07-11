"""This script will send you a picture from an amcrest camera if your phone
is not on the network while motion is detected.
"""
import argparse
import time

import telegram
from configparser import ConfigParser

from thief_snapshot import (
    cameras,
    presence_detection,
    motion_detection,
    logger,
)

# iPhones will occasionally drop off the network and then re-appear
MAX_DEVICE_MISSING_COUNT = 180

PHOTO_LIMIT = 10  # number of photos to take of the thief

CAMERA_CLASSES = {
    'amcrest': cameras.AmcrestCamera,
}

PRESENCE_DETECTOR_CLASSES = {
    'ddwrt': presence_detection.DDWRTPresenceDetector,
}

MOTION_DETECTOR_CLASSES = {
    'amcrest': motion_detection.AmcrestCameraMotionDetector,
}


def get_camera(settings):
    """Determines the camera class based on the camera type setting initializes
    it.
    """
    Camera = CAMERA_CLASSES.get(settings['camera']['type'])
    if Camera is None:
        raise Exception('Invalid camera_type setting.')

    return Camera(
        settings['camera']['ip'],
        int(settings['camera']['port']),
        settings['camera']['username'],
        settings['camera']['password'],
    )


def get_presence_detector(settings):
    """Determines the presence detector class based on the presence_detector
    type setting initializes it.
    """
    PresenceDetector = PRESENCE_DETECTOR_CLASSES.get(
        settings['presence_detector']['type']
    )
    if PresenceDetector is None:
        raise Exception('Invalid presence_detector type setting.')

    return PresenceDetector(
        settings['presence_detector']['ip'],
        int(settings['presence_detector']['port']),
        settings['presence_detector']['username'],
        settings['presence_detector']['password'],
        settings['presence_detector']['expected_macs'].split(','),
    )


def get_motion_detector(settings):
    """Determines the motion detector class based on the motion_detector type
    setting and initializes it.
    """
    MotionDetector = MOTION_DETECTOR_CLASSES.get(
        settings['motion_detector']['type']
    )
    if MotionDetector is None:
        raise Exception('Invalid motion_detector type setting.')

    return MotionDetector(
        settings['motion_detector']['ip'],
        int(settings['motion_detector']['port']),
        settings['motion_detector']['username'],
        settings['motion_detector']['password'],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help='Location of the config.ini file.')
    args = parser.parse_args()

    settings = ConfigParser()
    settings.read(args.config)

    presence_detector = get_presence_detector(settings)
    motion_detector = get_motion_detector(settings)
    camera = get_camera(settings)

    # TODO: support multiple notification systems
    bot = telegram.Bot(token=settings['telegram']['api_key'])

    device_missing_count = 0

    while True:
        presence_detected = presence_detector.is_presence_detected
        logger.info('Presence detected? %s', presence_detected)
        if presence_detected:
            device_missing_count = 0
        else:
            device_missing_count += 1
            logger.info('Presence undetected count: %s', device_missing_count)

        motion_detected = motion_detector.is_motion_detected
        logger.info('Motion detected? %s', motion_detected)

        if (device_missing_count > MAX_DEVICE_MISSING_COUNT) and motion_detected:
            for i in range(PHOTO_LIMIT):
                bot.send_photo(
                    chat_id=settings['telegram']['chat_id'],
                    photo=camera.snapshot(),
                )
                logger.info('Waiting between snapshots...')
                time.sleep(1)

            # give the telegram API a break
            time.sleep(30)

        logger.info('Waiting...')
        time.sleep(1)


if __name__ == "__main__":
    main()
