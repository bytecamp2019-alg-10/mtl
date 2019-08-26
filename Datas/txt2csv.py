cols = ['uid', 'user_city', 'item_id', 'author_id', 'item_city', 'channel', 'finish', 'like', 'music_id', 'device', 'time', 'duration']

def solve(ori, des):
    op = open(ori, 'r', encoding='utf8')
    wt = open(des, 'w', encoding='utf8')
    wt.write(','.join(cols) + '\r\n')
    for line in op.readlines():
        line = line.replace('\r', '').replace('\n', '').split('\t')
        wt.write(','.join(line) + '\r\n')
    op.close()
    wt.close()

def main():
    solve('../Datas/final_track2_train.txt', '../Datas/final_track2_train.csv')

if __name__ == '__main__':
    main()