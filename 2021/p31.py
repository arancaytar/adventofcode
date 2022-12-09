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
    def __init__(self, version, type, operands=None):
        self.version = version
        self.type = type
        self.operands = operands

def parse_packet(bits: BitStream) -> dict:
    packet = {}
    packet['version'] = bits.get(3)
    packet['type'] = bits.get(3)
    #print(f"Reading packet version {packet['version']} type {packet['type']}")
    if packet['type'] == 4:
        literal = 0
        continuity = bits.get(1)
        literal = literal << 4 | bits.get(4)
        while continuity:
            continuity = bits.get(1)
            literal = literal << 4 | bits.get(4)

        packet['literal'] = literal
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
        packet['operands'] = operands
    return packet

def versions(packet):
    yield packet['version']
    if packet['type'] != 4:
        for operand in packet['operands']:
            yield from versions(operand)

def read(hex):
    return parse_packet(BitStream.read(hex))

def solve1(hex):
    return sum(versions(read(hex)))

import sys
for line in sys.stdin:
    print(solve1(line))