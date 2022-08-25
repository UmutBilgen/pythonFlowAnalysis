from flow_future import FlowFuture
import pandas as pd
from last_future_name import LastFutureName


class WriteCsv:
    def __init__(self, future_dic):
        self.dic_to_csv(future_dic)

    def create_flow_future(self, future_dic):
        new_dic = {}
        for x, y in future_dic.items():
            new_dic[x] = FlowFuture(y)
        return new_dic

    def dic_to_csv(self, future_dic):
        dic = self.create_flow_future(future_dic)
        dic_list = []
        for value in dic.values():
            write_flows = LastFutureName()
            dic_list.append(write_flows.create(value))

        df = pd.DataFrame(dic_list)
        df.to_csv('deneme.csv')
