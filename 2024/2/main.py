import sys
from functools import reduce


def read():
	return [list(map(int, x.split())) for x in sys.stdin.read().split("\n")]
	
def diff(x: list):
    yield from (a-b for a,b in zip(x[1:], x[:-1]))

def minmax(x):
    a = b = next(x)
    return reduce(lambda cur,nex: (min(cur[0], nex), max(cur[1], nex)), x, (a,b))

def evaluate(report):
    a, b = minmax(diff(report))
    return a * b > 0 and max(abs(a), abs(b)) < 4

def evaluate_err(report, asc=True):
    for i in range(1, len(report)):
        diff = report[i] - report[i-1]
        if diff == 0 or (diff > 0) != asc or abs(diff) > 3:
            return i-1, i
    return False

def evaluate_damp(report):
    err = evaluate_err(report)
    if not err:
        return True
    a, b = err
    if not evaluate_err(report[:a] + report[a+1:]):
        return True
    if not evaluate_err(report[:b] + report[b+1:]):
        return True

    err = evaluate_err(report, False)
    if not err:
        return True
    a, b = err
    if not evaluate_err(report[:a] + report[a+1:], False):
        return True
    if not evaluate_err(report[:b] + report[b+1:], False):
        return True

    return False

def solve1(reports):
    return sum(map(evaluate, reports))

def solve2(reports):
    return sum(map(evaluate_damp, reports))

def main():
    reports = read()
    print(f"Problem 1: {solve1(reports)}")
    print(f"Problem 2: {solve2(reports)}")

def debug():
    reports = read()
    fixable = []
    unsafe = []
    safe = []
    fixable_or_safe = []
    for report in reports:
        a, b = evaluate(report), evaluate_damp(report)
        if not a and not b:
            unsafe.append(report)
        elif a and b:
            safe.append(report)
        elif a < b:
            fixable.append(report)
        else:
            raise ValueError(f"Safe report unfixable?? {report}")
        if b:
            fixable_or_safe.append(report)
    print(f"Unsafe {len(unsafe)}, safe {len(safe)}, fixable {len(fixable)}")
    print(f"Solution for 1: {len(safe)}, solution for 2: {len(fixable)+len(safe)}")
    print(f"Solution for 2: {len(fixable_or_safe)}")
    print(f"Solution for 2: {solve2(reports)}")
    

main()
#debug()