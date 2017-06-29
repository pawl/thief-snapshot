"""This script will send you a picture from an amcrest camera if your phone
is not on the network while motion is detected.
"""
import logging
import time

import telegram
from amcrest import AmcrestCamera

import settings
from ddwrt import is_mac_active

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

camera = AmcrestCamera(
    settings.camera_ip,
    80,
    settings.camera_username,
    settings.camera_password,
).camera

bot = telegram.Bot(token=settings.telegram_api_key)

# iPhones will occasionally drop off the network and then re-appear
MAX_DEVICE_MISSING_COUNT = 180

PHOTO_LIMIT = 10  # number of photos to take of the thief

device_missing_count = 0

while True:
    expected_mac_found = is_mac_active(settings.expected_mac)
    logging.info('Expected MAC address found? %s', expected_mac_found)
    if expected_mac_found:
        device_missing_count = 0
    else:
        device_missing_count += 1
        logging.info('MAC address missing count: %s', device_missing_count)

    motion_detected = camera.is_motion_detected
    logging.info('Motion detected? %s', motion_detected)

    if (device_missing_count > MAX_DEVICE_MISSING_COUNT) and motion_detected:
        for i in range(PHOTO_LIMIT):
            bot.send_photo(
                chat_id=settings.telegram_chat_id,
                photo=camera.snapshot(0),
            )
            logging.info('Waiting between snapshots...')
            time.sleep(1)

        # give the telegram API a break
        time.sleep(30)

    logging.info('Waiting...')
    time.sleep(1)
