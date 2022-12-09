import typing
from functools import reduce

class BitStream:
    def __init__(self, stream):
        self.stream = stream

    @staticmethod
    def read(hex: str):
        return BitStream(BitStream.combine(map(int, f"{c:0>4b}") for c in BitStream._hex(hex)))

    @staticmethod
    def _hex(hex: str):
        return map(lambda x: int(x, 16), hex)

    @staticmethod
    def combine(iterators):
        #print([list(iterator) for iterator in iterators])
        #raise ValueError()
        for iterator in iterators:
            yield from iterator

    def substream(self, k=1):
        return BitStream(self.take(k))

    def take(self, k=1):
        #print(list((c for i,c in zip(range(k), self.stream))))
        yield from (c for i,c in zip(range(k), self.stream))

    @staticmethod
    def decode(z) -> int:
        try:
            return reduce(lambda a, b: a << 1 | b, z)
        except TypeError:
            raise StopIteration("Out of bits")

    def get(self, k) -> int:
        return BitStream.decode(self.take(k))

class Packet:
    def __init__(self, version, type, literal=None, operands=None):
        self.version = version
        self.type = type
        self.literal = literal or 0
        self.operands = operands or []

    def evaluate(self):
        operands = (o.evaluate() for o in self.operands)
        match self.type:
            case 0:
                return sum(operands)
            case 1:
                return reduce(lambda a,b: a*b, operands)
            case 2:
                return min(operands)
            case 3:
                return max(operands)
            case 4:
                return self.literal
            case 5:
                return next(operands) > next(operands)
            case 6:
                return next(operands) < next(operands)
            case 7:
                return next(operands) == next(operands)

    def __str__(self):
        if self.type == 4:
            o = self.literal
            return f"Packet of type={self.type} version={self.version}: {o}"
        else:
            o = "\n" + "\n".join(str(o) for o in self.operands).replace("\n", "\n    ")
            return f"Packet of type={self.type} version={self.version}: {o}"


def parse_packet(bits: BitStream) -> Packet:
    v = bits.get(3)
    t = bits.get(3)
    #print(f"Reading packet version {packet['version']} type {packet['type']}")
    if t == 4:
        literal = 0
        continuity = bits.get(1)
        literal = literal << 4 | bits.get(4)
        while continuity:
            continuity = bits.get(1)
            literal = literal << 4 | bits.get(4)

        return Packet(v, t, literal=literal)
        #print(f"   Literal {packet['literal']}")
    else:
        operands = []
        length_type = bits.get(1)
        if length_type:
            packet_count = bits.get(11)
            for i in range(packet_count):
                operands.append(parse_packet(bits))
        else:
            bit_count = bits.get(15)
            #print(f"{bit_count} bits in the operands")
            subbits = bits.substream(bit_count)
            while True:
                try:
                    operands.append(parse_packet(subbits))
                except StopIteration:
                    break
        return Packet(v, t, operands=operands)

def versions(packet):
    yield packet.version
    if packet.type != 4:
        for operand in packet.operands:
            yield from versions(operand)

def read(hex) -> Packet:
    return parse_packet(BitStream.read(hex))

def solve1(hex):
    return sum(versions(read(hex)))

def solve2(hex):
    return read(hex).evaluate()

import sys
for line in sys.stdin:
    p = read(line)
    #print(p)
    print(p.evaluate())