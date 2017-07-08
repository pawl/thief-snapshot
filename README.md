# thief-snapshot

Detects motion with a camera and sends snapshots using a telegram chatbot if your phone is not on wifi.


Requirements
------------

* Amcrest Camera
* DD-WRT Router
* Telegram API Key & Chat ID


Installation
-----------

Install the package:

    $ pip install thief_snapshot[amcrest]

Generate a settings file:

    $ thief_snapshot_generate_settings

Edit the generated settings.ini and fill in your own settings.


Usage
-----------

    $ thief_snapshot settings.ini


TODO
----

* Add support for more cameras types.
* Add support for more presence detection types.
* Add more notification systems and make telegram notifications optional.

Credit
------

The ddwrt presence detection code was mostly copied from home-assistant.
