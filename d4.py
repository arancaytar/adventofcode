import sys
import re

def check(s):
    x = dict((x.split(':') for x in s.split()))
    if not {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'} <= x.keys():
        return False
    if not {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'} >= x.keys():
        return False
    if not 1920 <= int(x['byr']) <= 2002:
        return False
    if not 2010 <= int(x['iyr']) <= 2020:
        return False
    if not 2020 <= int(x['eyr']) <= 2030:
        return False
    m = re.match('^(.*)(cm|in)$', x['hgt'])
    if m is None:
        return False
    elif m.group(2) == 'cm' and not (150 <= int(m.group(1)) <= 193):
        return False
    elif not (59 <= int(m.group(1)) <= 76):
        return False
    if re.match('^#[a-f0-9]{6,6}$', x['hcl']) is None:
        return False
    if x['ecl'] not in {'amb','blu','brn','gry','grn','hzl','oth'}:
        return False
    if re.match('^\d{9,9}$', x['pid']) is None:
        return False
    return True


print(sum(check(s) for s in sys.stdin.read().split("\n\n")))