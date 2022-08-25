from internet_protocol import InternetProtocol


class DicAndIsForward:

    def create_dic(self, pcap_file):
        mac_inf = {}
        for packet in pcap_file:
            flow_list = []
            basic_inf = InternetProtocol()
            flows = basic_inf.type_protocol_flow(packet)
            if flows is not None:
                if mac_inf.get(flows.fwd_flow_id) is None and mac_inf.get(flows.bwd_flow_id) is None:
                    flows.is_forward = True
                    flow_list.append(flows)
                    mac_inf[flows.fwd_flow_id] = flow_list
                else:
                    flow_list = mac_inf.get(flows.fwd_flow_id)
                    if flow_list is None:
                        flows.is_forward = False
                        flow_list = mac_inf.get(flows.bwd_flow_id)
                        flow_list.append(flows)
                        mac_inf[flows.bwd_flow_id] = flow_list
                    else:
                        flows.is_forward = True
                        flow_list.append(flows)
                        mac_inf[flows.fwd_flow_id] = flow_list
        return mac_inf
