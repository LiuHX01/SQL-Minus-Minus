'''
CLOSURE(I):
    1.本身在其中
    2.若A->α·Bβ属于CLOSURE(I)，那么对于任何B->γ，项目B->·γ也属于其中
    3.反复迭代直到不再增多
'''
start_f = 'S~'

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
Go = {}
Vn = ['S~', 'E', 'A', 'B']
Vt = ['a', 'b', 'c', 'd']

ACTION = {}
GOTO = {}

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
# 作为框里的项
def get_CLOSURE(cnt):
    # 每次迭代都调用，直到不再增大
    # input: 当前迭代的CLOSURE [[左1, [右1], 点位置1], [左2, [右2], 点位置2]]
    def get_CLOSURE_I(Item):
        ret = Item.copy()
        # [左, 右, 点位置]
        for it in Item:
            left, rights, point = it[0], it[1], it[2]
            # 防止越界
            if point == len(rights):
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

    f = 1
    while f:
        f = 0
        len1 = len(Closure[cnt])
        Closure[cnt] = get_CLOSURE_I(Closure[cnt])
        len2 = len(Closure[cnt])

        if len2 > len1:
            f = 1


# 什么结构好呢- -
# GO = {(转移前序号, 转移符号): 转移后序号}
# 作为项集之间的连线


# 构造文法的LR(0)自动机
def get_FA():
    # 如果有一样的，那么自环，返回序号
    # 修改：是连接到已存在的项集
    def check(cur_count):
        for k, v in Closure.items():
            if k < cur_count:
                if v == Closure[cur_count]:
                    return k
        return -1


    # 项集总数，作为新项集的编号
    count = 1
    # 当前处理的项集编号
    curr = 0
    # 每一轮处理一个项集，当没有新增项集时自动机构造完成
    while curr < count:
        # print(curr, count)
        # 用该项集的初始内容构造项集
        if curr == 0:
            get_CLOSURE(curr)
        # 现在编号为curr的项集完整了
        # 接下来对于点右边每个符号进行GO
        # 不同符号分组 {'E': [[左, [右], 位置], [左, [右], 位置]]}
        to_deal = {}
        for each in Closure[curr]:
            left, rights, point = each[0], each[1], each[2]
            # 点右边没符号了
            if point == len(rights):
                # TODO:这里处理方式还没想好
                if left == start_f:
                    Go[(curr, '#')] = -2
                else:
                    Go[(curr, '#')] = -1
            else:
                # 点右边的符号
                to_move = rights[point]
                # 传统艺能，蠢写法
                tmp = to_deal.get(to_move).copy() if to_deal.get(to_move) is not None else []
                tmp.append([left, rights, point + 1])
                to_deal[to_move] = tmp

        # todeal 满了 可以分批送去当作初始项集
        for k, v in to_deal.items():
            Closure[count] = v
            get_CLOSURE(count)
            self_f = check(count)

            # 是一个新的
            if self_f == -1:
                Go[(curr, k)] = count
                count += 1
            else:
                Go[(curr, k)] = self_f
                del Closure[count]

        curr += 1


# ACTION = {(状态, 符号): 动作}
# 待定使用 GOTO = {(状态, 符号): 序号}
def get_lr0_analysis_table():
    for k, v in Closure.items():
        for each in v:
            left, rights, point = each[0], each[1], each[2]
            # A->α·aβ属于Ik且Go(Ik, a)=Ij ACTION[k, a]=sj
            if point < len(rights) and Go.get((k, rights[point])) is not None and rights[point] not in Vn:
                ACTION[(k, rights[point])] = 's' + str(Go[(k, rights[point])])

            # 项目A->α·属于Ik，对任何终结符和结束符a ACTION[k, a] == rj
            if point == len(rights) and left != start_f:
                # 寻找文法序号
                num = -1
                for gk, gv in Grammar.items():
                    if gk[1] == left and gv[0] == rights:
                        num = gk[0]
                        break
                for vt in Vt:
                    ACTION[(k, vt)] = 'r' + str(num)
                ACTION[(k, '#')] = 'r' + str(num)

            # 接受
            if left == start_f and point == 1:
                ACTION[(k, '#')] = 'acc'

            # Go(Ik, A)=Ij A为非终结符 GOTO[k, A]=j
            if left in Vn and Go.get((k, left)) is not None:
                GOTO[(k, left)] = Go[(k, left)]
        pass
    pass


if __name__ == '__main__':
    # get_grammar()
    get_FA()
    get_lr0_analysis_table()
    for k, v in ACTION.items():
        print(k, v)
    print('=======')
    for k, v in GOTO.items():
        print(k, v)
    # for k, v in Closure.items():
    #     print(k, v)
    # print('=======')
    # for k, v in Go.items():
    #     print(k, v)