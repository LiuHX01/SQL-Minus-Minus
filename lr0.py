Items = {(0, 'root~'): [['root'], [0, 1]]}


# Items = {(序号，左端): [['右端1', '右端2', '右端3'], [0, 1, 2, 3]}
def get_grammar():
    with open('data/grammar.txt', 'r', encoding='utf-8') as f:
        gs = f.readlines()

    for g in gs:
        if g[0] == '/':
            continue
        tmp = g.partition('.')
        seqnum = int(tmp[0])
        tmp = tmp[2].strip().partition(' -> ')
        left = tmp[0]
        rights = tmp[2]
        rightl = rights.split(' ')

        # 书中说：项集可以用一对整数来表示：（产生式编号，点的位置）
        # 这里和文法合并，将点位置含义设置为点前有几个符号
        pos = [x for x in range(len(rightl) + 1)]

        Items[(seqnum, left)] = [rightl, pos]


def get_CLOSURE():
    pass


def get_GOTO():
    pass


def get_ACTION():
    pass


if __name__ == '__main__':
    get_grammar()
    for k, v in Items.items():
        print(k, v)
