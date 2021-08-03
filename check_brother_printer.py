#!/usr/bin/python3

import argparse
import requests
import sys

FIELDS = {
    'Toner': ('% of Life Remaining(Toner)', '%'),
    'Drum': ('% of Life Remaining(Drum Unit)', '%'),
    'Page Counter': ('Page Counter', ''),
}

exit_status = 0

parser = argparse.ArgumentParser()
parser.add_argument('host', help='Printer to check.')
parser.add_argument('--drum-warn', help='Drum warning percent.')
parser.add_argument('--drum-crit', help='Drum critical percent.')
parser.add_argument('--toner-warn', help='Toner warning percent.')
parser.add_argument('--toner-crit', help='Toner critical percent.')
args = parser.parse_args()

if not args.host:
  parser.error('Must specify host.')
elif not args.drum_warn or not args.toner_warn:
  parser.error('Must specify warning levels.')
elif not args.drum_crit or not args.toner_crit:
  parser.error('Must specify critical levels.')

try:
  csv = requests.get(f'http://{args.host}/etc/mnt_info.csv').text.rstrip()
except:
  sys.exit(3)
csv = csv.replace('"', '')
k, v = [x.split(',') for x in csv.split('\n')]
data = dict(zip(k, v))

s = []
for name, (key, unit) in FIELDS.items():
  s.append(f'{name}: {data[key]}{unit}')
output = ', '.join(s)

lookup = lambda x: int(data[FIELDS[x][0]])
if (int(args.drum_crit) >= lookup('Drum') or
    int(args.toner_crit) >= lookup('Toner')):
  output = f'CRITICAL: {output}'
  exit_status = 2
elif (int(args.drum_warn) >= lookup('Drum') or
    int(args.toner_warn) >= lookup('Toner')):
  output = f'WARNING: {output}'
  exit_status = 1
else:
  output = f'OK: {output}'
print(output)
sys.exit(exit_status)
