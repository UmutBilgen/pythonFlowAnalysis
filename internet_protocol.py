from flow_mac_inf import FlowMacInfo


class InternetProtocol:
    def __init__(self):
        self.flags = {
            'F': 'FIN',
            'S': 'SYN',
            'R': 'RST',
            'P': 'PSH',
            'A': 'ACK',
            'U': 'URG',
            'E': 'ECE',
            'C': 'CWR',
        }
        self.ipv4 = False
        self.ipv6 = False
        self.check = True

    def check_proto(self, packet):
        if 'ICMP' in packet:
            self.check = False

    def check_address(self, packet):
        if "IPv6" in packet:
            self.ipv6 = True
            self.ipv4 = False

        elif "IP" in packet:
            self.ipv6 = False
            self.ipv4 = True

    def ipv6_packet(self, packet):
        new_packet = FlowMacInfo()
        new_packet.src = packet.src
        new_packet.dst = packet.dst
        new_packet.src_ip = packet['IPv6'].src
        new_packet.dst_ip = packet['IPv6'].dst
        new_packet.protocol = packet[2].name
        new_packet.src_port = packet[new_packet.protocol].sport
        new_packet.dst_port = packet[new_packet.protocol].dport
        new_packet.timestamp = packet.time
        new_packet.idle = packet.hlim
        new_packet.payload_bytes = len(packet[new_packet.protocol].payload)
        new_packet.header_bytes = packet[1].len
        if packet[2].name == "TCP":
            new_packet.tcp_window = packet.window
        return new_packet

    def ipv4_packet(self, packet):
        new_packet = FlowMacInfo()
        new_packet.src = packet.src
        new_packet.dst = packet.dst
        new_packet.src_ip = packet['IP'].src
        new_packet.dst_ip = packet['IP'].dst
        new_packet.protocol = packet[2].name
        if self.check:
            new_packet.src_port = packet[new_packet.protocol].sport
            new_packet.dst_port = packet[new_packet.protocol].dport
        new_packet.timestamp = packet.time
        new_packet.idle = packet[1].ttl
        new_packet.payload_bytes = len(packet[new_packet.protocol].payload)
        new_packet.header_bytes = packet[1].len
        if packet[2].name == "TCP":
            new_packet.tcp_window = packet.window
            flags_name = [self.flags[x] for x in packet.sprintf('%TCP.flags%')]
            for i in range(len(flags_name)):
                match flags_name[i]:
                    case 'FIN':
                        new_packet.flags = ['FIN', 1]
                    case 'SYN':
                        new_packet.flags = ['SYN', 1]
                    case 'RST':
                        new_packet.flags = ['RST', 1]
                    case 'PSH':
                        new_packet.flags = ['PSH', 1]
                    case 'ACK':
                        new_packet.flags = ['ACK', 1]
                    case 'URG':
                        new_packet.flags = ['URG', 1]
                    case 'ECE':
                        new_packet.flags = ['ECE', 1]
                    case 'CWR':
                        new_packet.flags = ['CWR', 1]
        return new_packet

    def type_protocol_flow(self, packet):
        self.check_address(packet)
        self.check_proto(packet)
        if self.ipv4 and self.check:
            return self.ipv4_packet(packet)
        elif self.ipv6 and self.check:
            return self.ipv6_packet(packet)
        else:
            return None
