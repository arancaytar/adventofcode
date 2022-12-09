def simulation(initial, reset, start, days):
    state = [0] * (max(start, reset) + 1)
    for x in initial:
        state[x] += 1
    for day in range(days):
        zero = state[0]
        state = state[1:] + [0]
        state[reset] += zero
        state[start] += zero
    return sum(state)

state = list(map(int, input().split(",")))

print(simulation(state, 6, 8, 80))