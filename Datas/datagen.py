import random

op = open('./final_track2_train.csv', 'r', encoding='utf8')
lines = op.readlines()
title = lines[0]
lines = lines[1:]
op.close()

number = len(lines)
spl_num = number // 10
small_num = 100

index = [i for i in range(number)]
random.shuffle(index)

outs = []
outs.append(('test', index[:spl_num]))
outs.append(('vali', index[spl_num: 2 * spl_num]))
outs.append(('train', index[2 * spl_num:]))
smi = index[2 * spl_num:]
random.shuffle(smi)
outs.append(('small_test', smi[:small_num]))
outs.append(('small_vali', smi[small_num: 2 * small_num]))
outs.append(('small_train', smi[2 * small_num: 12 * small_num]))

for unit in outs:
    wt = open('./' + unit[0] + '.csv', 'w', encoding='utf8')
    wt.write(title)
    for id in unit[1]:
        wt.write(lines[id])
    wt.close()
