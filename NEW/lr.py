import sys
import functions


def get_fa(grammar: dict, first: dict, syntax_type: int, start: str):
    """得到一个自动机，迭代得到closure，过程中得到go

    :param first: {l: ['r1', 'r2', 'r3', '$']}
    :param start: 'root'
    :param grammar: {(seq_num, l): [['r1', 'r2', 'r3'], [0, 1, 2, 3(点前符号数)]]}
    :param syntax_type: 1/2/3
    :return: closure: {序号: [[左端, [右端], 点位置], [左端, [右端], 点位置]]}
             LR1: {序号: [[左端, [右端], 点位置, ['vt1', 'vt2']]]}
             go: {(转移前序号，转移符号): 转移后序号}
    """
    closure, go = {}, {}

    def get_closure(cnt: int):
        """通过迭代不断增大所求项集

        :param cnt: 所求项集编号
        :return: 完整项集
        """

        def get_closure_i(Item: list):
            """对于closure的某一项，每次迭代都调用，直到不再增大

            :param Item: closure某一项的value部分
            :return: 当前轮数迭代下closure该项的扩充结果
            """
            ret = Item.copy()
            for it in Item:
                left, rights, point = it[0], it[1], it[2]
                if point == len(rights):
                    continue
                # 点的后一个符号
                to_find = rights[point]

                # 在规则中找
                for gk, gv in grammar.items():
                    if gk[1] == to_find:
                        if gv[0] == ['$']:
                            continue
                        # 找到左端是点后符号，将点在最左的右端加入
                        if (syntax_type == 1 or syntax_type == 2) and [to_find, gv[0], 0] not in ret:
                            ret.append([to_find, gv[0], 0])
                        elif syntax_type == 3:
                            alphas = it[3]
                            beta = rights[point + 1: len(rights)]
                            tmp_vt = []
                            # 对于LR1，要求每个的 点后符号后串 + c/d 的first集
                            for alpha in alphas:
                                first_ab = functions.get_str_first(beta + [alpha], first)
                                tmp_vt += first_ab
                                tmp_vt = list(set(tmp_vt))
                            if [to_find, gv[0], 0, tmp_vt] not in ret:
                                ret.append([to_find, gv[0], 0, tmp_vt])
            return ret

        f = 1
        while f:
            f = 0
            len1 = len(closure[cnt])
            closure[cnt] = get_closure_i(closure[cnt])
            len2 = len(closure[cnt])

            if len2 > len1:
                f = 1

    # 检查当前的项集是否已存在，存在返回序号
    def check(cur_count: int):
        for ck, cv in closure.items():
            if ck < cur_count:
                if cv == closure[cur_count]:
                    return ck
        return -1

    # 此处开始-----------------------------------------------------
    if syntax_type == 1 or syntax_type == 2:
        closure[0] = [[start, grammar[(0, start)][0], 0]]
    elif syntax_type == 3:
        closure[0] = [[start, grammar[(0, start)][0], 0, ['#']]]

    # 项集总数，作为新项集的编号
    count = 1
    # 当前处理的项集编号
    curr = 0

    # 每一轮处理一个项集，当没有新增项集时自动机构造完成
    while curr < count:
        if curr == 0:
            get_closure(curr)

        # 可能同一个左端有多个右端，故分组 {'E': [[左, [右], 位置], [左, [右], 位置]]}
        to_deal = {}
        for each in closure[curr]:
            left, rights, point = each[0], each[1], each[2]
            # 点右边没符号了
            if point == len(rights):
                # 暂时这样处理，貌似对后面分析表的构造没有影响
                if left == start:
                    go[(curr, '#')] = -2
                else:
                    go[(curr, '#')] = -1
            else:
                # 点右边的符号
                to_move = rights[point]
                # 得到待移动符号的
                tmp = to_deal.get(to_move).copy() if to_deal.get(to_move) is not None else []
                if syntax_type == 1 or syntax_type == 2:
                    tmp.append([left, rights, point + 1])
                elif syntax_type == 3:
                    vts = each[3]
                    tmp.append([left, rights, point + 1, vts])
                to_deal[to_move] = tmp

        # to deal 满了 可以送去当作初始项集
        for k, v in to_deal.items():
            closure[count] = v
            get_closure(count)
            self_f = check(count)

            # 是一个新的
            if self_f == -1:
                go[(curr, k)] = count
                count += 1
            # 新项集等于已存在项集，直接连线
            else:
                go[(curr, k)] = self_f
                del closure[count]

        curr += 1

    return closure, go


def get_pred_anal_table(grammar: dict, follow: dict, closure: dict, go: dict, vn: list, vt: list, start: str,
                        syntax_type: int):
    action, goto = {}, {}

    for k, v in closure.items():
        for each in v:
            left, rights, point = each[0], each[1], each[2]

            # A->α·aβ属于Ik且Go(Ik, a)=Ij ACTION[k, a]=sj
            if point < len(rights) and go.get((k, rights[point])) is not None and rights[point] in vt:
                action[(k, rights[point])] = 's' + str(go[(k, rights[point])])

            # 项目A->α·属于Ik，对任何终结符和结束符a ACTION[k, a] == rj，SLR和LR1需额外判断
            if point == len(rights) and left != start:
                # 寻找文法序号
                num = -1
                for gk, gv in grammar.items():
                    if gk[1] == left and gv[0] == rights:
                        num = gk[0]
                        break
                if syntax_type == 1 or syntax_type == 2:
                    for t in vt:
                        # slr
                        if syntax_type == 2:
                            if t in follow[left]:
                                action[(k, t)] = 'r' + str(num)
                                continue
                            else:
                                continue
                        action[(k, t)] = 'r' + str(num)
                    action[(k, '#')] = 'r' + str(num)
                # lr1
                elif syntax_type == 3:
                    vts = each[3]
                    for t in vts:
                        action[(k, t)] = 'r' + str(num)

            # 接受
            if left == start and point == 1:
                action[(k, '#')] = 'acc'

            # Go(Ik, A)=Ij A为非终结符 GOTO[k, A]=j
            if left in vn and go.get((k, left)) is not None:
                goto[(k, left)] = go[(k, left)]

    return action, goto


def reduce(token: list, grammar: dict, action: dict, goto: dict):
    cnt = 1
    state_stack = [0]
    ch_stack = ['#']
    token.append(['#', '#'])

    for in_str, in_type in token:
        # 关键字、运算符、界符，输入符号是本身
        if in_type == 'KW' or in_type == 'OP' or in_type == 'SE':
            to_deal = in_str
        else:
            to_deal = in_type

        f = 1
        while f:
            f = 0
            state_stack_top = state_stack[-1]
            ch_stack_top = ch_stack[-1]

            # 先得到表内符号
            try:
                act = action[(state_stack_top, to_deal)]
            except KeyError:
                print(f'ERROR:{state_stack_top}, {to_deal}')
                print(state_stack, ch_stack)
                sys.exit()

            # 接受
            if act == 'acc':
                print(f'{cnt}\t/\t{ch_stack_top}#{to_deal}\taccept')
                break
            # 移入
            elif act[0] == 's':
                print(f'{cnt}\t/\t{ch_stack_top}#{to_deal}\tmove')
                state_stack.append(int(act[1:]))
                ch_stack.append(to_deal)
                cnt += 1

            # 规约需要：1.改变符号栈 2.弹出状态栈 3.根据新状态栈顶、新符号栈顶、GOTO确定入栈状态
            elif act[0] == 'r':
                rule_num = int(act[1:])
                print(f'{cnt}\t{rule_num}\t{ch_stack_top}#{to_deal}\treduction')

                # 找到该规则对应右部
                left, rights = '', []
                for k, v in grammar.items():
                    if k[0] == rule_num:
                        left, rights = k[1], v[0]

                # 注意符号栈里的是规则右部，需要替换为左部，先弹出右部数量的符号
                for i in range(len(rights)):
                    ch_stack.pop()
                    state_stack.pop()
                ch_stack.append(left)

                try:
                    state_stack.append(goto.get((state_stack[-1], ch_stack[-1])))
                except KeyError:
                    print('ERROR:找不到GOTO项')
                    sys.exit()

                f = 1
                cnt += 1

            else:
                print(act)
                sys.exit()
