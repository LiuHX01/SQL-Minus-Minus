'''
CLOSURE(I):
    1.本身在其中
    2.若A->α·Bβ属于CLOSURE(I)，那么对于任何B->γ，项目B->·γ也属于其中
    3.反复迭代直到不再增多
'''
import sys

start_f = 'S~'

Grammar = {(0, 'root~'): [['root'], [0, 1]]}
# Grammar = {
#     (0, 'S~'): [['E'], [0, 1]],
#     (1, 'E'): [['a', 'A'], [0, 1, 2]],
#     (2, 'E'): [['b', 'B'], [0, 1, 2]],
#     (3, 'A'): [['c', 'A'], [0, 1, 2]],
#     (4, 'A'): [['d'], [0, 1]],
#     (5, 'B'): [['c', 'B'], [0, 1, 2]],
#     (6, 'B'): [['d'], [0, 1]]
# }
Grammar = {
    (0, 'S~'): [['E'], [0, 1]],
    (1, 'E'): [['E', '+', 'T'], [0, 1, 2, 3]],
    (2, 'E'): [['T'], [0, 1]],
    (3, 'T'): [['T', '*', 'F'], [0, 1, 2, 3]],
    (4, 'T'): [['F'], [0, 1]],
    (5, 'F'): [['(', 'E', ')'], [0, 1, 2, 3]],
    (6, 'F'): [['id'], [0, 1]]
}
# Grammar = {
#     (0, 'S~'): [['S'], [0, 1]],
#     (1, 'S'): [['a', 'A', 'c', 'B', 'e'], [0, 1, 2, 3, 4, 5]],
#     (2, 'A'): [['b'], [0, 1]],
#     (3, 'A'): [['A', 'b'], [0, 1, 2]],
#     (4, 'B'): [['d'], [0, 1]]
# }
# Closure = {0: [['root~', ['root'], 0]]}
# Closure = {1: [['root', ['dmlStatement'], 0]]}
Closure = {
    0: [['S~', ['E'], 0]]
}
# Closure = {
#     0: [['S~', ['S'], 0]]
# }
Go = {}
Vn = ['S~', 'E', 'T', 'F']
# Vn = ['S~', 'S', 'A', 'B']
# Vt = ['a', 'b', 'c', 'd', 'e']
# Vn = []
# Vt = []
Vt = ['+', '*', '(', ')', 'id']

ACTION = {}
GOTO = {}



Follow = {
    'S~': ['#'],
    'E': [')', '+', '#'],
    'T': [')', '+', '*', '#'],
    'F': [')', '+', '*', '#']
}


slr_flag = 1


# Grammar = {(序号, 左端): [['右端1', '右端2', '右端3'], [0, 1, 2, 3]]}
def get_grammar():
    with open('../data/grammar.txt', 'r', encoding='utf-8') as f:
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

        # 得到非终结符
        Vn.append(left)

        if rightl == ['$']:
            # 对于A->ε，只有A->·
            pos = [-1]
        else:
            # 书中说：项集可以用一对整数来表示：（产生式编号，点的位置）
            # 这里和文法合并，将点位置含义设置为点前有几个符号
            pos = [x for x in range(len(rightl) + 1)]

        Grammar[(seqnum, left)] = [rightl, pos]

    # 得到终结符
    for k, v in Grammar.items():
        for each in v[0]:
            if each not in Vn and each != '$' and each not in Vt:
                Vt.append(each)


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
                    # slr
                    if slr_flag and vt in Follow[left]:
                        ACTION[(k, vt)] = 'r' + str(num)
                        continue
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


# 我们假设Token和LL1一样的格式
def reduce(Token):
    cnt = 1
    state_stack = [0]
    ch_stack = ['#']

    for in_str, in_type in Token:
        # 关键字、运算符、界符，输入符号是本身
        if in_type == 'KW' or in_type == 'OP' or in_type == 'SE':
            todeal = in_str
        else:
            todeal = in_type

        f = 1
        while f:
            f = 0
            state_stack_top = state_stack[-1]
            ch_stack_top = ch_stack[-1]

            # 先得到表内符号
            try:
                action = ACTION[(state_stack_top, todeal)]
            except:
                print(f'ERROR:{state_stack_top}, {todeal}')
                print(state_stack, ch_stack)
                sys.exit()
            # print(f'ACT:{action}，面临输入：{todeal}')
            # print(f'状态栈：{state_stack}')
            # print(f'符号栈：{ch_stack}')
            # 接受
            if action == 'acc':
                print(f'{cnt}\t/\t{ch_stack_top}#{todeal}\taccept')
                break
            # 移入
            elif action[0] == 's':
                print(f'{cnt}\t/\t{ch_stack_top}#{todeal}\tmove')
                state_stack.append(int(action[1:]))
                ch_stack.append(todeal)
                cnt += 1
                pass
            # 规约需要：1.改变符号栈 2.弹出状态栈 3.根据新状态栈顶、新符号栈顶、GOTO确定入栈状态
            elif action[0] == 'r':
                rule_num = int(action[1:])
                print(f'{cnt}\t{rule_num}\t{ch_stack_top}#{todeal}\treduction')
                # 找到该规则对应右部 出现弊端
                left, rights = '', []
                for k, v in Grammar.items():
                    if k[0] == rule_num:
                        left, rights = k[1], v[0]
                # 注意符号栈里的是规则右部，需要替换为左部，先弹出右部数量的符号
                # 4.15修改：正确做法 先弹出r长度
                for i in range(len(rights)):
                    ch_stack.pop()
                    state_stack.pop()
                ch_stack.append(left)

                try:
                    state_stack.append(GOTO.get((state_stack[-1], ch_stack[-1])))
                except:
                    print('ERROR:找不到GOTO项')
                    sys.exit()

                f = 1
                cnt += 1
                pass
            else:
                print(action)
                sys.exit()

        pass
    pass


if __name__ == '__main__':
    # get_grammar()
    # print(Vt)
    get_FA()
    get_lr0_analysis_table()
    for k, v in ACTION.items():
        print(k, v)
    print('=======')
    for k, v in Go.items():
        print(k, v)
    print('=======')
    for k, v in Closure.items():
        print(k, v)

    # print('=======')
    # for k, v in Go.items():
    #     print
    # reduce([['a', 'a'], ['b', 'b'], ['b', 'b'], ['c', 'c'], ['d', 'd'], ['e', 'e'], ['#', '#']])
    reduce([['id', 'id'], ['*', '*'], ['id', 'id'], ['+', '+'], ['id', 'id'], ['#', '#']])
    # reduce([['SELECT', 'KW'], ['t', 'IDN'], ['.', 'OP'], ['c', 'IDN'], ['FROM', 'KW'], ['t', 'IDN'], ['WHERE', 'KW'], ['t', 'IDN'], ['.', 'OP'],
    #         ['a', 'IDN'], ['>', 'OP'], ['0', 'INT'], ['#', '#']])