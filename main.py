from scapy.all import rdpcap
from dic_and_isForward import DicAndIsForward
from write_csv import WriteCsv


if __name__ == '__main__':
    pcap_file = rdpcap('tcpcap.pcap')
    mac_inf = {}
    dic_and_isForward = DicAndIsForward()
    mac_inf = DicAndIsForward().create_dic(pcap_file)
    WriteCsv(mac_inf)

