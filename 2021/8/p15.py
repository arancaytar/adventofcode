from collections import Counter
lengths = Counter()
while True:
    try:
        signal, display = input().split(" | ")
        lengths += Counter(map(len, display.split()))
    except:
        break

print(sum(lengths[i] for i in (2, 4, 3, 7)))
