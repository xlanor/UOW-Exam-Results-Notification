# UOW-Exam-Results-Notification
A personal tg bot to tell me when my results are out, because for some reason I dont get notified when exam results are out.

Read the comments.

Scrapes UOW SOLS.

You need to run this on your own.

Uses selenium + chrome headless, so you will need to have chrome installed.

Requires ptb, selenium, python >= 3.4

Get chromedriver from [here](https://chromedriver.storage.googleapis.com/index.html?path=2.36/) , dont fuck with the permissions or it will segfault.

If running from remote server, please add --no-sandbox params into chrome options in the script.

Also added a systemd unit to be placed in /lib/systemd/service. Change the user and group.

Note that you shouldnt be running user as root, chrome cannot be run as root.

If you don't know how to run this, this probably isn't meant for you to use it...

Written in approx 1h+, tested on 
- arch linux w / Google Chrome 65.0.3325.146 | Python 3.6.4 | Selenium v 3.10.0
- Ubuntu 16.04 xenial w/ Google Chrome 65.0.3325.146 | Python 3.5.2  | Selenium v 3.10.0 ( headless config )
