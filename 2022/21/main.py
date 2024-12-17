import sys

def readgraph(data):
    lines = [x.split(": ") for x in data.split("\n")]
    graph = {}
    for node, rhs in lines:
        t = rhs.split()
        if len(t) == 3:
            op = (t[1], t[0], t[2])
        else:
            op = int(t[0])
        graph[node] = op
    return graph

def evaluate(graph):
    evaluated = {}
    def evaluate_(node):
        if node not in evaluated:
            if type(graph[node]) is int:
                evaluated[node] = graph[node]
            else:
                operator, operand1, operand2 = graph[node]
                evaluated[node] = int(eval(f"{evaluate_(operand1)} {operator} {evaluate_(operand2)}"))
        return evaluated[node]
    return evaluate_('root')

def calculate_operands(op, a, b, result):
    if op == '+':
        if a is None:
            return result - b
        elif b is None:
            return result - a
    elif op == '-':
        if a is None:
            return result + b
        elif b is None:
            return a - result
    elif op == '*':
        if a is None:
            return result // b
        elif b is None:
            return result // a
    elif op == '/':
        if a is None:
            return result * b
        elif b is None:
            return a // result
    raise ValueError(f"Unknown operator {op}, or over-defined operands {a} and {b}.")

def evaluate_force(graph):
    evaluated = {}
    def evaluate_(node, result=None):
        #print(node, result, node in evaluated)
        if node not in evaluated:
            if node == 'root':
                operator, operand1, operand2 = graph[node]
                #print(f"{operand1} == {operand2}")
                a = evaluate_(operand1)
                b = evaluate_(operand2)
                if type(a) is int:
                    b = evaluate_(operand2, a)
                elif type(b) is int:
                    #print(operand1, a, operand2, b)
                    a = evaluate_(operand1, b)
                else:
                    raise ValueError("Insufficient data for a meaningful answer. Both operands contain unknown variable.")
                return a == b
            elif node == 'humn':
                if result:
                    evaluated[node] = result
                return result
            elif type(graph[node]) is int:
                if result is not None and result != graph[node]:
                    raise ValueError(f"Cannot make constant {graph[node]} equal {result}.")
                evaluated[node] = graph[node]
                return evaluated[node]
            else:
                operator, operand1, operand2 = graph[node]
                #print("   ", node, '=', operator, operand1, operand2)
                a = evaluate_(operand1)
                b = evaluate_(operand2)
                #print("   ", node, '=', result, "<-", operator, a, b)
                if result:
                    if type(a) == int and b is None:
                        b = calculate_operands(operator, a, b, result)
                        evaluate_(operand2, b)
                    elif a is None and type(b) == int:
                        #print(f"Calculating ? {operator} {b} = {result}")
                        a = calculate_operands(operator, a, b, result)
                        evaluate_(operand1, a)
                        #print(a)
                if type(a) == type(b) == int:
                    #print("   ", node, '=', result, "<-", operator, a, b)
                    evaluated[node] = int(eval(f"{a} {operator} {b}"))
                    if result is not None and result != evaluated[node]:
                        raise ValueError(f"Cannot make {evaluated[node]} equal {result}.")
                    return evaluated[node]
                return None
        return evaluated[node]
    evaluate_('root')
    return evaluated['humn']

def solve1(data):
    graph = readgraph(data)
    return evaluate(graph)

def solve2(data):
    graph = readgraph(data)
    return evaluate_force(graph)


data = sys.stdin.read().strip()
print(solve1(data))
print(solve2(data))