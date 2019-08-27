import pandas as pd

filepath = '~/workspace/Datasets/ByteCamp/data.train'
limit = 50

people_region_dict = {
    'uid' : 'u_region_id',
    'author_id' : 'g_region_id'
}

class SF:
    def __init__(self):
        self.df = pd.read_csv(filepath, dtype=int)
        self.dic = {}
        self.dic['uid'] = {}
        self.dic['author_id'] = {}
        self.area_average = {}
        self.PreProcess()

    def update(self, row, name):
        key = row[name]
        if not key in self.dic[name].keys():
            self.dic[name][key] = {}
            self.dic[name][key]['area'] = row[people_region_dict[name]]
            for types in ['like', 'finish']:
                self.dic[name][key][types] = {
                    'count' : 0,
                    'action' : 0,
                    'sum_of_duration' : 0
                }
        for types in ['like', 'finish']:
            self.dic[name][key][types]['count'] += 1
            if row[types] == 1:
                self.dic[name][key][types]['action'] += 1
                self.dic[name][key][types]['sum_of_duration'] += row['duration']

    def update(self, name, area, types, rat, avg):
        self.area_average[name][area][types]['ratio'] *= self.area_average[name][area][types]['count']
        self.area_average[name][area][types]['average'] *= self.area_average[name][area][types]['average']
        self.area_average[name][area][types]['ratio'] += rat
        self.area_average[name][area][types]['average'] += avg
        self.area_average[name][area][types]['count'] += 1.0
        self.area_average[name][area][types]['ratio'] /= self.area_average[name][area][types]['count']
        self.area_average[name][area][types]['average'] /= self.area_average[name][area][types]['count']

    def PreProcess(self):
        for row in self.df.rows:
            self.update(row, 'uid')
            self.update(row, 'author_id')
        for name in ['uid', 'authod_id']:
            self.area_average[name] = {}
            for key in range(2):
                self.area_average[name][key] = {}
                for types in ['like', 'finish']:
                    self.area_average[name][key][types] = {}
                    for dat in ['ratio', 'average', 'count']:
                        self.area_average[name][key][types][dat] = 0.0
            for key in self.dic[name].keys():
                for types in ['like', 'finish']:
                    tmp_dict = self.dic[name][key][types]
                    self.dic[name][key][types]['ratio'] = float(tmp_dict['action']) / float(tmp_dict['count'])
                    self.dic[name][key][types]['average'] = float(tmp_dict['sum_of_duration']) / float(tmp_dict['count'])
                    self.update(
                        name,
                        self.dic[name][key]['area'],
                        types,
                        self.dic[name][key][types]['ratio'],
                        self.dic[name][key][types]['average']
                    )

    def GetResult(self, row):
        F = []
        for name in ['uid', 'author_id']:
            for types in ['finish', 'like']:
                for results in ['ratio', 'average']:
                    if not row[name] in self.dic[name].keys() or self.dic[name][row[name]][types]['count'] <= limit:
                        F.append(self.area_average[name][people_region_dict[name]][types][results])
                    else:
                        F.append(self.dic[name][row[name]][types][results])
        return F

def test():
    sf = SF()
    print(sf.GetResult(sf.df[3]))

if __name__ == '__main__':
    test()