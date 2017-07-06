# Zordon Telegram Bot
_Gathers together the most powerful kittens, pandas and capybaras in the Universe to fight with evil and boredom. Or, at least, to play Overwatch._

[![Build Status](https://travis-ci.org/KrusnikViers/Zordon.svg?branch=master&style=flat)](https://travis-ci.org/KrusnikViers/Zordon)
[![Build Status](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://opensource.org/licenses/MIT)

**Dependencies:**
* Python 3.3 or newer
* PostgreSQL 9.2 or newer
* Packages from `requirements.txt`

**Environment variables:**

* `TELEGRAM_TOKEN`\
Access token for Telegram Bot.\
Should be received from @BotFather during bot registration.

* `DATABASE_URL`\
DSN-formatted complete URL of PostgreSQL database.\
DSN-format: `postgres://<user>:<password>@<host>:<port>/<database_name>`.

* `SUPERUSER_LOGIN`\
Username (without @) of only user with unlimited access

* `COOLDOWN_TIME` (optional)\
Duration (in minutes) of time period, while user considered as participant of activity.

* `WEBHOOK_URL` (optional)\
URL of the Zordon server.\
If set, bot will run in webhook mode, instead of usual polling.
