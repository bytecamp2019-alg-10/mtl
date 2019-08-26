import pandas as pd

cols = ['uid', 'user_city', 'item_id', 'author_id', 'item_city', 'channel', 'finish', 'like', 'music_id', 'device', 'time', 'duration']

num_list = ['duration']
cat_list = ['uid', 'user_city', 'item_id', 'author_id', 'item_city', 'channel', 'music_id', 'device', 'time']
lab_list = ['finish', 'like']

class DatAna:
    def __init__(self, file):
        self.df = pd.read_csv(file, dtype='category')
        for col in num_list:
            self.df[col].astype('float')
        self.res = pd.DataFrame(self.df, lab_list, dtype='category')
        self.df.drop(lab_list, axis=1)
        self.res = pd.get_dummies(self.res)

    def describe(self):
        pd.describe(self.df).apply(lambda s : s.apply(lambda x : format(x, 'f')))

def main():
    da = DatAna('../Datas/train.csv')
    da.describe()

if __name__ == '__main__':
    main()