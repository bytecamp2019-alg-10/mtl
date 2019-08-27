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
        self.area = {}

    def PreProcess(self):
        for name in ['uid', 'author_id']:
            self.area[name] = {}
            for types in ['finish', 'like']:
                self.area[name][types] = {}
                for id in range(2):
                    self.area[name][types][id] = {}
                    # ratio
                    self.area[name][types][id]['ratio'] = float(
                        self.df[self.df[people_region_dict[name]] == id & self.df[types] == 1].shape[0]) / float(
                        self.df[self.df[people_region_dict[name]] == id].shape[0])
                    # average
                    self.area[name][types][id]['ratio'] = float(
                        self.df[self.df[people_region_dict[name]] == id & self.df[types] == 1].apply(sum)['duration']) / float(
                        self.df[self.df[people_region_dict[name]] == id].shape[0])

    def statics(self, row, name, types):
        ret = []
        # ratio
        try:
            if self.df[name == row[name]].shape[0] > limit:
                ret.append(float(self.df[self.df[name] == row & self.df[self.df[types]] == 1].shape[0]) / float(self.df[self.df[name] == row[name]].shape[0]))
            else:
                ret.append(self.area[row[people_region_dict[name]]]['ratio'])
        except Exception as ex:
            ret.append(self.area[row[people_region_dict[name]]]['ratio'])

        # average
        try:
            if self.df[name == row[name]].shape[0] > limit:
                ret.append(float(self.df[self.df[name] == row & self.df[self.df[types]] == 1].apply(sum)['duration']) / float(
                    self.df[self.df[name] == row & self.df[self.df[types]] == 1].shape[0]))
            else:
                ret.append(self.area[name][types][row[people_region_dict[name]]]['ratio'])
        except Exception as ex:
            ret.append(self.area[name][types][row[people_region_dict[name]]]['ratio'])
        return ret

    def GetResult(self, row):
        F = []
        for name in ['uid', 'author_id']:
            for types in ['finish', 'like']:
                for val in self.statics(row, name, types):
                    F.append(val)
        return F

def test():
    sf = SF()
    print(sf.GetResult(sf.df[3]))

if __name__ == '__main__':
    test()