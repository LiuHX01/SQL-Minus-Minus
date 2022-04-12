# Grammar = {(0, 'root~'): [['root'], [0, 1]]}
Grammar = {
    (0, 'S~'): [['E'], [0, 1]],
    (1, 'E'): [['a', 'A'], [0, 1, 2]],
    (2, 'E'): [['b', 'B'], [0, 1, 2]],
    (3, 'A'): [['c', 'A'], [0, 1, 2]],
    (4, 'A'): [['d'], [0, 1]],
    (5, 'B'): [['c', 'B'], [0, 1, 2]],
    (6, 'B'): [['d'], [0, 1]]
}
# Closure = {0: [['root~', ['root'], 0]]}
# Closure = {1: [['root', ['dmlStatement'], 0]]}
Closure = {
    0: [['S~', ['E'], 0]]
}
GO = {}

# Grammar = {(序号, 左端): [['右端1', '右端2', '右端3'], [0, 1, 2, 3]]}
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

        if rightl == ['$']:
            # 对于A->ε，只有A->·
            pos = [-1]
        else:
            # 书中说：项集可以用一对整数来表示：（产生式编号，点的位置）
            # 这里和文法合并，将点位置含义设置为点前有几个符号
            pos = [x for x in range(len(rightl) + 1)]

        Grammar[(seqnum, left)] = [rightl, pos]


# CLOSURE: {序号: [[左1, [右1], 点位置1], [左2, [右2], 点位置2]]}
# Item
def get_CLOSURE():
    # 每次迭代都调用，直到不再增大
    # input: 当前迭代的CLOSURE [[左1, [右1], 点位置1], [左2, [右2], 点位置2]]
    def get_CLOSURE_I(Item):
        ret = Item.copy()
        # [左, 右, 点位置]
        for it in Item:
            left, rights, point = it[0], it[1], it[2]
            if point == len(rights) + 1:
                continue
            # 点的后一个符号
            to_find = rights[point]
            # 在规则中找
            for gk, gv in Grammar.items():
                if gk[1] == to_find:
                    if gv[0] == ['$']:
                        continue
                    if [to_find, gv[0], 0] not in ret:
                        ret.append([to_find, gv[0], 0])
        return ret

    # TODO:对于每个项集
    f = 1
    while f:
        f = 0
        len1 = len(Closure[0])
        Closure[0] = get_CLOSURE_I(Closure[0])
        len2 = len(Closure[0])

        if len2 > len1:
            f = 1
    print(Closure[0])
    pass


def get_GOTO():
    pass


def get_ACTION():
    pass


if __name__ == '__main__':
    # get_grammar()
    get_CLOSURE()
