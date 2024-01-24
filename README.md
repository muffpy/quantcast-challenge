# Quantcast challenge

## Challenge

Given a cookie log file in the following format:
```
cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00
AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00
4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00
fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00
4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00
```

Write a command line program in your preferred language to process the log file and return the most active
cookie for a specific day. Please include a -f parameter for the filename to process and a -d parameter to
specify the date.

e.g. we’d execute your program like this to obtain the most active cookie for 9th Dec 2018.

```
$ ./[command] -f cookie_log.csv -d 2018-12-09
AtY0laUfhglK3lC7
```

## Contents
`data/`: input files for testing

`most_active_cookie.py`: one-off CLI script which reads cookie log (*.csv) and prints most seen cookie(s) on specific date 

`tests.py`: unit tests written using pytest

## Dependencies
https://github.com/pytest-dev/pytest

## Usage
```
$ python3 most_active_cookie.py -f data/cookie-log.csv -d 2018-12-08
SAZuXPGUrfbcn5UA
4sMM2LxV07bPJzwf
fbcn5UAVanZf6UtG
```

## Tests
```
pytest -v tests.py
```
