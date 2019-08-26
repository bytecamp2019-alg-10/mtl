import random
import pandas as pd

def Split_DF(df, rat):
    rows = df.shape[0]
    train_rows = int(rows * rat)
    indexs = [i for i in range(rows)]
    random.shuffle(indexs)
    pd.DataFrame(df, rows=indexs[:train_rows]).to_csv('./train_' + str(int(rat * 10)) + '.csv', index=0)
    pd.DataFrame(df, rows=indexs[train_rows:]).to_csv('./vali_' + str(int(rat * 10)) + '.csv', index=0)

def main():
    df = pd.read_csv('./bytecamp.data', dtype=int)
    df_before = pd.DataFrame()
    df_test = pd.DataFrame()
    for line_id in range(df.shape[0]):
        if df['date'][line_id] == 20190708:
            df_test.append(df.loc[line_id, :])
        else:
            df_before.append(df.loc[line_id, :])
    df_test.to_csv('test.csv', index=0)
    Split_DF(df_before, 0.7)
    Split_DF(df_before, 0.8)
    Split_DF(df_before, 0.9)

if __name__ == '__main__':
    main()