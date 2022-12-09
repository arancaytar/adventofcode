import re
import sys

def check(a, b, letter, word):
    return int(a) <= sum(letter == x for x in word) <= int(b)

def check2(a, b, letter, word):
    return (word[int(a)-1] == letter) != (word[int(b)-1] == letter)

def a1(lines):
    return sum(check(*re.split('[: -] *', line)) for line in lines)

def a2(lines):
    return sum(check2(*re.split('[: -] *', line)) for line in lines)

print(a2(sys.stdin.read().split("\n")))