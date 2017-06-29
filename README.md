# thief-snapshot

Watches for motion on an amcrest camera and notifies you using telegram if your phone is not on the network.


Requirements
-----------

* Amcrest Camera
* DD-WRT Router
* Telegram API Key & Chat ID


Installation
-----------

First you will need to copy example_settings.py to settings.py:

    $ cp example_settings.py settings.py

Once the copy is complete, you will need to fill settings.py with your own information.

Next, you will need to install the requirements:

    $ pip install -r requirements.txt


Usage
-----------

    $ python main.py
