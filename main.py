"""This script will send you a picture from an amcrest camera if your phone
is not on the network while motion is detected.
"""
import logging
import time
import subprocess

import telegram
from amcrest import AmcrestCamera

import settings

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
MAX_PING_FAIL_COUNT = 180

PHOTO_LIMIT = 10  # number of photos to take of the thief


def detect_expected_ip():
    """Pings the expected_ip in settings.py to see if the device is present.

    Credit to homeassistant's device_tracker/ping.py
    """
    ping_cmd = ['ping', '-n', '-q', '-c1', '-W1', settings.expected_ip]

    pinger = subprocess.Popen(ping_cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL)
    try:
        pinger.communicate()
        return pinger.returncode == 0
    except subprocess.CalledProcessError:
        return False


ping_fail_count = 0

while True:
    expected_ip_found = detect_expected_ip()
    logging.info('Expected IP found? %s', expected_ip_found)
    if expected_ip_found:
        ping_fail_count = 0
    else:
        ping_fail_count += 1
        logging.info('Ping failure count: %s', ping_fail_count)

    motion_detected = camera.is_motion_detected
    logging.info('Motion detected? %s', motion_detected)

    if (ping_fail_count > MAX_PING_FAIL_COUNT) and motion_detected:
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
