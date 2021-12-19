import functools
from queue import LifoQueue


def compute_expression(hex_expression):
    bin_str = hex_to_binary_string(hex_expression)
    packets = parse_packets(bin_str)
    values = [p.get_value() for p in packets]
    if len(values) == 1:
        return values[0]
    else:
        return values


hex_to_bin = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}


def hex_to_binary_string(hex_str):
    bin_str = ""
    for h in hex_str:
        bin_str += hex_to_bin[h]
    return bin_str


op_codes = {
    0: lambda *args: sum(args),
    1: lambda *args: functools.reduce(lambda a, b: a * b, args),
    2: lambda *args: min(args),
    3: lambda *args: max(args),

    # ops with exactly two subpackets
    5: lambda a, b: 1 if a > b else 0,
    6: lambda a, b: 1 if a < b else 0,
    7: lambda a, b: 1 if a == b else 0
}


class Packet:
    def __init__(self, version, type_id, value=None):
        self.version = version
        self.type_id = type_id
        self.value = value
        self.sub_packets = []

    def __repr__(self):
        s = f"{self.version}-{self.type_id}: {self.value}"
        for p in self.sub_packets:
            s += f"\n\t-> {p}"
        return s

    def get_value(self):
        if self.value:
            return self.value
        else:
            return op_codes.get(self.type_id)(
                *[sp.get_value() for sp in self.sub_packets]
            )

    @staticmethod
    def from_bin_string(bin_str):
        try:
            version = int(bin_str[0:3], 2)
            type = int(bin_str[3:6], 2)
            remaining_string = bin_str[6:]

            if type == 4:  # parse packet as literal value
                value_bits = ""
                read_str = remaining_string

                while read_str:
                    value_bits += read_str[1:5]
                    if read_str[0] == "0":  # last group in value
                        read_str = ""
                    else:
                        read_str = read_str[5:]
                    remaining_string = remaining_string[5:]
                value = int(value_bits, 2)
                return Packet(version, type, value), remaining_string
            else:  # parse packet as operator
                length_type_id = remaining_string[0]
                remaining_string = remaining_string[1:]
                new_packet = Packet(version, type)
                if length_type_id == "0":
                    length_bits = 15
                    length = int(remaining_string[:length_bits], 2)
                    subpacket_str = remaining_string[length_bits:(length_bits + length)]
                    remaining_string = remaining_string[length_bits + length:]
                    sub_packets = parse_packets(subpacket_str)
                    for sp in sub_packets:
                        if sp is not None:
                            new_packet.sub_packets.append(sp)
                else:
                    length_bits = 11
                    num_packets = int(remaining_string[:length_bits], 2)
                    remaining_string = remaining_string[length_bits:]
                    while remaining_string and len(new_packet.sub_packets) < num_packets:
                        sp, remaining_string = Packet.from_bin_string(remaining_string)
                        new_packet.sub_packets.append(sp)

                return new_packet, remaining_string
        except (IndexError, ValueError):
            return None, ""


def parse_packets(bin_str):
    packets = []
    while len(bin_str) > 0:
        packet, bin_str = Packet.from_bin_string(bin_str)
        if packet:
            packets.append(packet)

    return packets


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        hex_str = f.read().strip()
        bin_str = hex_to_binary_string(hex_str)
        packets = parse_packets(bin_str)

        version_sum = 0
        packet_queue = LifoQueue()

        for p in packets:
            packet_queue.put(p)

        while not packet_queue.empty():
            p: Packet = packet_queue.get()
            version_sum += p.version
            for sp in p.sub_packets:
                packet_queue.put(sp)

        print(f"Sum of all packet version numbers: {version_sum}")

        result = compute_expression(hex_str)
        print(f"Computed result from hex expression = {result}")
