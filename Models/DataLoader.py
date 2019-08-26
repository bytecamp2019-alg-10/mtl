import os
import numpy as np

class DataLoader():
    def __init__(self, path, pre, suf, pred, types, need_vali = False): # pred is a list counts from 0-based
        self.pred = pred
        self.types = types
        self.cate_dict = None
        self.train = self.readfile(path + pre + 'train' + suf)
        self.test = self.readfile(path + pre + 'test' + suf)
        self.vali = None
        if need_vali:
            self.vali = self.readfile(path + pre + 'vali' + suf, pred)
        print(len(self.train[0][0]))

    def solve_onehot(self, s, t):
        if t == 'bool':
            if s == '0':
                return [1, 0]
            else:
                return [0, 1]
        return None

    def solve(self, id, s, t):
        if t == 'int':
            r = [0 for i in range(len(self.cate_dict[id].keys()))]
            r[self.cate_dict[id][int(s)]] = 1
            return r
        else:
            return [float(s)]

    def readfile(self, name):
        op = open(name, 'r', encoding='utf8')
        lines = op.readlines()
        d = []
        r = []
        for line in lines:
            spl = line.replace('\r', '').replace('\n', '').split('\t')
            ret = []
            for id in range(len(spl)):
                if id in self.pred:
                    ret.append( self.solve_onehot(spl[id], self.types[id]) )
            r.append(ret)
        self.cate_dict = {}
        for feat_id in range(len(self.types)):
            if feat_id in self.pred:
                continue
            dic = {}
            cnt = 0
            for line in lines:
                spl = line.replace('\r', '').replace('\n', '').split('\t')
                # print(line)
                feat_val = int(spl[feat_id])
                if not feat_val in dic.keys():
                   dic[feat_val] = cnt
                   cnt += 1
            self.cate_dict[feat_id] = dic
        for line in lines:
            spl = line.replace('\r', '').replace('\n', '').split('\t')
            dat = []
            for id in range(len(spl)):
                if id not in self.pred:
                    for num in self.solve(id, spl[id], self.types[id]):
                        dat.append(num)
            d.append(dat)
        return (d, r)

def main():
    tps = ['int', 'int', 'int', 'int', 'int', 'int', 'bool', 'bool', 'int', 'int', 'int', 'float']
    d = DataLoader('../Datas/', '', '.txt', [6, 7], tps, True)

if __name__ == '__main__':
    main()