# Cron job parser

## About The Project
Joyful command line application which parses a cron jobs and displays the perioud the task will run. 

This program was a task for the internship. Parses all subset of minutes, hours, days of month, months and days of week except special strings as "@yearly", "L", "W", "?", "#".

Uses recursive calls to parse complex combinations

## Installation and Run

```bash
git clone https://github.com/Torogeldiev-T/cron_parser.git
cd cron_parser
py ./main.py "*/15 0 1,15 */5,8 1-5 /usr/bin/find"
```
##  Input
There is an example of input
```bash
py ./main.py "*/15 0 1,15 */5,8 1-5 /usr/bin/find"
```
## Output
```bash
minute: 0 15 30 45
hour: 0
day of month: 1 15
month: 5 8 10
day of week: 1 2 3 4 5
command: /usr/bin/find
```
## Testing

```bash
cd cron_parser
py -m unittest tests.py -f
```

Should output the following:
```bash
........
----------------------------------------------------------------------
Ran 8 tests in 0.002s

OK
```
