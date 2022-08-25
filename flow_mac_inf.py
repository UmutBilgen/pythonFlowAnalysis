class FlowMacInfo:

    def __init__(self):
        self.__src = None
        self.__dst = None
        self.__src_port = None
        self.__dst_port = None
        self.__src_ip = None
        self.__dst_ip = None
        self.__protocol = None
        self.__timestamp = None
        self.__payload_bytes = None
        self.__payload_packet = 0
        self.__header_bytes = None
        self.__is_forward = None
        self.__fwd_flow_id = None
        self.__bwd_flow_id = None
        self.__flags = {}
        self.__tcp_window = 0
        self.__idle = 0

    @property
    def src(self):
        return self.__src

    @src.setter
    def src(self, src):
        self.__src = src

    @property
    def dst(self):
        return self.__dst

    @dst.setter
    def dst(self, dst):
        self.__dst = dst

    @property
    def src_port(self):
        return self.__src_port

    @src_port.setter
    def src_port(self, src_port):
        self.__src_port = src_port

    @property
    def dst_port(self):
        return self.__dst_port

    @dst_port.setter
    def dst_port(self, dst_port):
        self.__dst_port = dst_port

    @property
    def src_ip(self):
        return self.__src_ip

    @src_ip.setter
    def src_ip(self, src_ip):
        self.__src_ip = src_ip

    @property
    def dst_ip(self):
        return self.__dst_ip

    @dst_ip.setter
    def dst_ip(self, dst_ip):
        self.__dst_ip = dst_ip

    @property
    def protocol(self):
        return self.__protocol

    @protocol.setter
    def protocol(self, proto):
        self.__protocol = proto

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, ts):
        self.__timestamp = ts

    @property
    def payload_bytes(self):
        return self.__payload_bytes

    @payload_bytes.setter
    def payload_bytes(self, payload_bytes):
        self.__payload_bytes = payload_bytes

    @property
    def payload_packet(self):
        self.__payload_packet += 1
        return self.payload_packet

    @payload_packet.setter
    def payload_packet(self, payload_packet):
        self.__payload_packet = payload_packet

    @property
    def header_bytes(self):
        return self.__header_bytes

    @header_bytes.setter
    def header_bytes(self, header_bytes):
        self.__header_bytes = header_bytes

    @property
    def fwd_flow_id(self):
        self.__fwd_flow_id = str(self.src_ip) + ':' + str(self.src_port) + '>' + str(self.dst_ip) + ':' + str(
            self.dst_port) + '--' + str(self.protocol)
        return self.__fwd_flow_id

    @fwd_flow_id.setter
    def fwd_flow_id(self, fwd_flow_id):
        self.__fwd_flow_id = fwd_flow_id

    @property
    def bwd_flow_id(self):
        self.__bwd_flow_id = str(self.dst_ip) + ':' + str(self.dst_port) + '>' + str(self.src_ip) + ':' + str(
            self.src_port) + '--' + str(self.protocol)
        return self.__bwd_flow_id

    @bwd_flow_id.setter
    def bwd_flow_id(self, bwd_flow_id):
        self.__bwd_flow_id = bwd_flow_id

    @property
    def flags(self):
        return self.__flags

    @flags.setter
    def flags(self, key_value):
        self.__flags[key_value[0]] = key_value[1]

    @property
    def tcp_window(self):
        return self.__tcp_window

    @tcp_window.setter
    def tcp_window(self, tcp_window):
        self.__tcp_window = tcp_window

    @property
    def is_forward(self):
        return self.__is_forward

    @is_forward.setter
    def is_forward(self, forward_is):
        self.__is_forward = forward_is

    @property
    def idle(self):
        return self.__idle

    @idle.setter
    def idle(self, set_idle):
        self.__idle = set_idle
