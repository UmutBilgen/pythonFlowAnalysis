from statistics import mean, pstdev, variance
from datetime import datetime


class FlowFuture:

    def __init__(self, y):
        self.flow_mac_inf = y
        self.__flow_duration = None
        self.__flow_bytes_duration = None
        self.__fwd_per_sec = None
        self.__bwd_per_sec = None
        self.__down_up_ratio = None
        self.__avg_packet_size = None
        self.__fwd_avg_segment_size = None
        self.__bwd_avg_segment_size = None
        self.__sflow_fwd_bytes = None
        self.__sflow_fwd_packet = None
        self.__sflow_bwd_bytes = None
        self.__sflow_bwd_bytes = None
        self.__packet_count = None

    @property
    def src(self):
        return self.flow_mac_inf[0].src

    @property
    def dst(self):
        return self.flow_mac_inf[0].dst

    @property
    def src_port(self):
        return self.flow_mac_inf[0].src_port

    @property
    def dst_port(self):
        return self.flow_mac_inf[0].dst_port

    @property
    def src_ip(self):
        return self.flow_mac_inf[0].src_ip

    @property
    def dst_ip(self):
        return self.flow_mac_inf[0].dst_ip

    @property
    def protocol(self):
        return self.flow_mac_inf[0].protocol

    @property
    def timestamp(self):
        return datetime.fromtimestamp(float(self.flow_mac_inf[-1].timestamp))

    @property
    def flow_id(self):
        return self.flow_mac_inf[0].fwd_flow_id

    @property
    def flow_duration(self):
        time_max = 0
        time_min = 9999999999999999999999999999
        for flow in self.flow_mac_inf:
            if time_max < flow.timestamp:
                time_max = flow.timestamp

            if time_min > flow.timestamp:
                time_min = flow.timestamp

        self.__flow_duration = float(time_max - time_min) * 1000000
        return self.__flow_duration

    @property
    def flow_bytes_duration(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            temp_list.append(flow.payload_bytes)
        if self.flow_duration > 0:
            self.__flow_bytes_duration = sum(temp_list) / self.flow_duration
        return self.__flow_bytes_duration

    @property
    def forward_packet_second(self):
        count = 0
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                count += 1
        if self.flow_duration > 0:
            self.__fwd_per_sec = count / self.flow_duration
        return self.__fwd_per_sec

    @property
    def backward_packet_second(self):
        count = 0
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                count += 1
        if self.flow_duration > 0:
            self.__bwd_per_sec = count / self.flow_duration
        return self.__bwd_per_sec

    @property
    def down_up_ratio(self):
        count_fwd = 0
        count_bwd = 0
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                count_bwd += 1
            else:
                count_fwd += 1
        self.__down_up_ratio = count_bwd / count_fwd
        return self.__down_up_ratio

    @property
    def avg_packet_size(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            temp_list.append(flow.payload_bytes)
        self.__avg_packet_size = sum(temp_list) / len(self.flow_mac_inf)
        return self.__avg_packet_size

    @property
    def fwd_avg_segment_size(self):
        temp_list = []
        count = 0
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.payload_bytes)
                count += 1
        self.__fwd_avg_segment_size = sum(temp_list) / count
        return self.__fwd_avg_segment_size

    @property
    def bwd_avg_segment_size(self):
        temp_list = []
        count = 0
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.payload_bytes)
                count += 1
        self.__bwd_avg_segment_size = sum(temp_list) / count
        return self.__bwd_avg_segment_size

    @property
    def sflow_fwd_bytes(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.payload_bytes)

        self.__sflow_fwd_bytes = sum(temp_list) / len(self.flow_mac_inf)
        return self.__sflow_fwd_bytes

    @property
    def sflow_fwd_packet(self):
        count = 0
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                count += 1

        self.__sflow_fwd_packet = count / len(self.flow_mac_inf)
        return self.__sflow_fwd_packet

    def sflow_bwd_bytes(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.payload_bytes)

        self.__sflow_bwd_bytes = sum(temp_list) / len(self.flow_mac_inf)
        return self.__sflow_bwd_bytes

    @property
    def sflow_bwd_packet(self):
        count = 0
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                count += 1

        self.__sflow_bwd_bytes = count / len(self.flow_mac_inf)
        return self.__sflow_bwd_bytes

    @property
    def packet_count(self):
        self.__packet_count = len(self.flow_mac_inf)
        return self.__packet_count

    # FORWARD BACKWARD STATUTORILY
    @property
    def forward_bulk_duration_in_second(self):
        time_max = 0
        time_min = 9999999999999999999999999999
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                if time_max < flow.timestamp:
                    time_max = flow.timestamp

                if time_min > flow.timestamp:
                    time_min = flow.timestamp
        return time_max - time_min

    @property
    def forward_avg_bytes_per_bulk(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.payload_bytes)

        return sum(temp_list) / (len(temp_list) / 4)

    @property
    def forward_avg_packet_per_bulk(self):
        temp_list = []
        count = 0
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                count += 1
                temp_list.append(count)

        return sum(temp_list) / (len(temp_list) / 4)

    @property
    def forward_avg_bulk_rate(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if self.forward_bulk_duration_in_second > 0:
            return float(sum(temp_list)) / float(self.forward_bulk_duration_in_second)
        else:
            return 0

    ###################
    @property
    def backward_bulk_duration_in_second(self):
        time_max = 0
        time_min = 9999999999999999999999999999
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                if time_max < flow.timestamp:
                    time_max = flow.timestamp

                if time_min > flow.timestamp:
                    time_min = flow.timestamp
        return time_max - time_min

    @property
    def backward_avg_bytes_per_bulk(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if len(temp_list) > 0:
            return sum(temp_list) / (len(temp_list) / 4)
        else:
            return 0

    @property
    def backward_avg_packet_per_bulk(self):
        temp_list = []
        count = 0
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                count += 1
                temp_list.append(count)
        if len(temp_list) > 0:
            return sum(temp_list) / (len(temp_list) / 4)
        else:
            return 0

    @property
    def backward_avg_bulk_rate(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if self.forward_bulk_duration_in_second > 0:
            return float(sum(temp_list)) / float(self.backward_bulk_duration_in_second)

    @property
    def flow_active(self):
        temp_list = []
        count = 0
        for flow in self.flow_mac_inf:
            temp_list.append(flow.timestamp)
            if len(self.flow_mac_inf) == 1:
                temp_list[0] = 0
            if count == len(self.flow_mac_inf):
                temp_list[count] = 0
            if count >= 1:
                temp_list[count - 1] = temp_list[count] - temp_list[count - 1]
            count += 1
        temp_list[-1] = 0
        return temp_list

    @property
    def forward_active_time(self):
        temp_list = []
        count = 0
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.timestamp)
                if len(self.flow_mac_inf) == 1:
                    temp_list[0] = 0
                elif count == len(self.flow_mac_inf):
                    temp_list[count] = 0
                elif count >= 1:
                    temp_list[count - 1] = temp_list[count] - temp_list[count - 1]
                count += 1
        temp_list[-1] = 0
        return temp_list

    @property
    def backward_active_time(self):
        temp_list = []
        count = 0
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.timestamp)
                if len(self.flow_mac_inf) == 1:
                    temp_list[0] = 0
                elif count == len(self.flow_mac_inf):
                    temp_list[count] = 0
                elif count >= 1:
                    temp_list[count - 1] = temp_list[count] - temp_list[count - 1]
                count += 1
        if count > 0:
            temp_list[-1] = 0
        return temp_list

    @property
    def total_fwd_packets(self):
        count = 0
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                count += 1
        return count

    @property
    def total_bwd_packets(self):
        count = 0
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                count += 1
        return count

    @property
    def total_length_bwd_packets(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.payload_bytes)
        return sum(temp_list)

    @property
    def total_length_fwd_packets(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.payload_bytes)
        return sum(temp_list)

    @property
    def total_length_fwd_packets_max(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if len(temp_list) > 0:
            return max(temp_list)
        else:
            return 0

    @property
    def total_length_bwd_packets_max(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if len(temp_list) > 0:
            return max(temp_list)
        else:
            return 0

    @property
    def total_length_fwd_packets_min(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if len(temp_list) > 0:
            return min(temp_list)
        else:
            return 0

    @property
    def total_length_bwd_packets_min(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if len(temp_list) > 0:
            return min(temp_list)
        else:
            return 0

    @property
    def total_length_fwd_packets_mean(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if len(temp_list) > 0:
            return mean(temp_list)
        else:
            return 0

    @property
    def total_length_bwd_packets_mean(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if len(temp_list) > 0:
            return mean(temp_list)
        else:
            return 0

    @property
    def total_length_fwd_packets_std(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if len(temp_list) > 0:
            return pstdev(temp_list)
        else:
            return 0

    @property
    def total_length_bwd_packets_std(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.payload_bytes)
        if len(temp_list) > 0:
            return pstdev(temp_list)
        else:
            return 0

    # IAT bosta gecen sure olabilir YANİ [0-1] arasında 3 saniye varsa list[0] = 3

    @property
    def flow_iat_avg(self):
        if (
                len(self.forward_active_time) > 0
                or
                len(self.backward_active_time) > 0
        ):
            total_at = self.forward_active_time + self.backward_active_time

            return mean(total_at)
        else:
            return 0

    @property
    def flow_iat_std(self):
        if (
                len(self.forward_active_time) > 0
                or
                len(self.backward_active_time) > 0
        ):
            total_at = self.forward_active_time + self.backward_active_time
            return pstdev(total_at)
        else:
            return 0

    @property
    def flow_iat_max(self):
        if (
                len(self.forward_active_time) > 0
                or
                len(self.backward_active_time) > 0
        ):
            total_at = self.forward_active_time + self.backward_active_time
            return max(total_at)
        else:
            return 0

    @property
    def flow_iat_min(self):
        if (
                len(self.forward_active_time) > 0
                or
                len(self.backward_active_time) > 0
        ):
            total_at = self.forward_active_time + self.backward_active_time
            return min(total_at)
        else:
            return 0

    @property
    def fwd_iat_total(self):
        if len(self.forward_active_time) > 0:
            return sum(self.forward_active_time)
        else:
            return 0

    @property
    def bwd_iat_total(self):
        if len(self.backward_active_time) > 0:
            return sum(self.backward_active_time)
        else:
            return 0

    @property
    def fwd_iat_mean(self):
        if len(self.forward_active_time) > 0:
            return mean(self.forward_active_time)
        else:
            return 0

    @property
    def bwd_iat_mean(self):
        if len(self.backward_active_time) > 0:
            return mean(self.backward_active_time)
        else:
            return 0

    @property
    def fwd_iat_std(self):
        if len(self.forward_active_time) > 0:
            return pstdev(self.forward_active_time)
        else:
            return 0

    @property
    def bwd_iat_std(self):
        if len(self.backward_active_time) > 0:
            return pstdev(self.backward_active_time)
        else:
            return 0

    @property
    def fwd_iat_max(self):
        if len(self.forward_active_time) > 0:
            return max(self.forward_active_time)
        else:
            return 0

    @property
    def bwd_iat_max(self):
        if len(self.backward_active_time) > 0:
            return max(self.backward_active_time)
        else:
            return 0

    @property
    def fwd_iat_min(self):
        if len(self.forward_active_time) > 0:
            return min(self.forward_active_time)
        else:
            return 0

    @property
    def bwd_iat_min(self):
        if len(self.backward_active_time) > 0:
            return min(self.backward_active_time)
        else:
            return 0

    @property
    def total_flags(self):
        total_flag_dic = {
            'FIN': 0,
            'SYN': 0,
            'RST': 0,
            'PSH': 0,
            'ACK': 0,
            'URG': 0,
            'ECE': 0,
            'CWR': 0,
        }
        for flow in self.flow_mac_inf:
            for x, y in flow.flags.items():
                total_flag_dic[x] += 1

        return total_flag_dic

    @property
    def total_backward_flags(self):
        forward_flag_dic = {
            'FIN': 0,
            'SYN': 0,
            'RST': 0,
            'PSH': 0,
            'ACK': 0,
            'URG': 0,
            'ECE': 0,
            'CWR': 0,
        }
        for flow in self.flow_mac_inf:
            for x, y in flow.flags.items():
                if flow.is_forward:
                    forward_flag_dic[x] += 1

        return forward_flag_dic

    @property
    def total_forward_flags(self):
        backward_flag_dic = {
            'FIN': 0,
            'SYN': 0,
            'RST': 0,
            'PSH': 0,
            'ACK': 0,
            'URG': 0,
            'ECE': 0,
            'CWR': 0,
        }
        for flow in self.flow_mac_inf:
            for x, y in flow.flags.items():
                if not flow.is_forward:
                    backward_flag_dic[x] += 1

        return backward_flag_dic

    @property
    def fwd_header_byte(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.header_bytes)

        return temp_list

    @property
    def bwd_header_byte(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.header_bytes)
        return temp_list

    @property
    def min_packet_length(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            temp_list.append(flow.payload_bytes)

        return min(temp_list)

    @property
    def max_packet_length(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            temp_list.append(flow.payload_bytes)

        return max(temp_list)

    @property
    def mean_packet_length(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            temp_list.append(flow.payload_bytes)

        return mean(temp_list)

    @property
    def std_packet_length(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            temp_list.append(flow.payload_bytes)

        return pstdev(temp_list)

    @property
    def variance_packet_length(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            temp_list.append(float(flow.payload_bytes))
        try:
            if sum(temp_list) > 0 and len(temp_list) > 0:
                return variance(temp_list)
        except:
            return 0

    # get parameter
    def get_forward_flag_count(self, key):
        temp_dic = self.total_forward_flags
        return temp_dic.get(key)

    def get_backward_flag_count(self, key):
        temp_dic = self.total_backward_flags
        return temp_dic.get(key)

    @property
    def init_win_bytes_forward(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.tcp_window)

        return sum(temp_list)

    @property
    def init_win_bytes_backward(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.tcp_window)

        return sum(temp_list)

    @property
    def ack_data_pkt_forward(self):
        count = 0
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                if flow.protocol == 'TCP' and flow.payload_bytes >= 1:
                    count += 1
        return count if count > 0 else 0

    @property
    def ack_data_pkt_backward(self):
        count = 0
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                if flow.protocol == 'TCP' and flow.payload_bytes >= 1:
                    count += 1
        return count if count > 0 else 0

    @property
    def min_segment_size_backward(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if not flow.is_forward:
                temp_list.append(flow.header_bytes)
        return min(temp_list) if len(temp_list) > 0 else 0

    @property
    def min_segment_size_forward(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            if flow.is_forward:
                temp_list.append(flow.header_bytes)
        return min(temp_list) if len(temp_list) > 0 else 0

    @property
    def flow_idle(self):
        temp_list = []
        for flow in self.flow_mac_inf:
            temp_list.append(flow.idle)
        return temp_list

    @property
    def idle_mean(self):
        return mean(self.flow_idle) if len(self.flow_idle) > 0 else 0

    @property
    def idle_std(self):
        return pstdev(self.flow_idle) if len(self.flow_idle) > 0 else 0

    @property
    def idle_min(self):
        return min(self.flow_idle) if len(self.flow_idle) > 0 else 0

    @property
    def idle_max(self):
        return max(self.flow_idle) if len(self.flow_idle) > 0 else 0

    @property
    def active_mean(self):
        return mean(self.flow_active) if len(self.flow_active) > 0 else 0

    @property
    def active_std(self):
        return pstdev(self.flow_active) if len(self.flow_active) > 0 else 0

    @property
    def active_min(self):
        return min(self.flow_active) if len(self.flow_active) > 0 else 0

    @property
    def active_max(self):
        return max(self.flow_active) if len(self.flow_active) > 0 else 0
