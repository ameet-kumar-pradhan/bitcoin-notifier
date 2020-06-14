# bitcoin-notifier

---

A Python script to send push notification to mobile device and telegram with help of IFTTT notifications.

---

## DESCRIPTION

---

Bitcoin price is a fickle thing. You never really know where it’s going to be at the end of the day. So, instead of constantly checking various sites for the latest updates, let’s make a Python app to do the work for you.

We’re going to use the popular automation website IFTTT.

We’re going to create there IFTTT applets:

One for emergency notification when Bitcoin price falls under a certain threshold and
one for regular Telegram and one for Slack updates on the Bitcoin price.

These will be triggered by our Python app which will consume the data from the Coindesk API.

An IFTTT applet is composed of two parts: a trigger and an action.

Trigger will be a webhook service provided by IFTTT.

Our Python app will make an HTTP request to the webhook URL which will trigger an action. Now, this is the fun part—the action could be almost anything you want. IFTTT offers a multitude of actions like sending an email, updating a Google Spreadsheet and even calling your phone.

---

## INSTALLATION

---

You might need to do these installations

1. Install python version 3

This website will help you find all the versions available as per your system requirments.Install python3.

https://www.python.org/downloads/

2. Installation for PIP for windows

```
pip install
```

Refer this website for further read
https://pip.pypa.io/en/stable/installing/

3. Dependencies

The only dependency is on the requests library.

```
pip install requests==2.18.4
```

---

## USAGE

---

Following query on terminal will provide you with all the help options

### INPUT

bitcoin-notifier -h

### OUTPUT

usage: bitcoin-notifier -e 10000 -t 1 [-h][-d decision] [-t interval][-e threshold]

### HELP

Bitcoin Notifier

optional arguments:
-h, --help show this help message and exit
-e threshold Enter threshold
-t interval Enter time interval
-d decision Enter (Yes/No) - Yes will run the program

This will provide 5 prices of Bitcoin, at the specified time interval according to the code.
