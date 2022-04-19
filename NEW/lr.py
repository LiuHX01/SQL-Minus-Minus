import sys
import functions


def get_fa(grammar: dict, first: dict, syntax_type: int, start: str):
    """得到一个自动机

    :param first:
    :param start:
    :param grammar:
    :param syntax_type:
    :return: closure: {序号: [[左端, [右端], 点位置], [左端, [右端], 点位置]]}
             LR1: {序号: [[左端, [右端], 点位置, ['vt1', 'vt2']]]}
             go: {(转移前序号，转移符号): 转移后序号}
    """
    closure, go = {}, {}

    def get_closure(cnt):
        # 每次迭代都调用，直到不再增大
        # input: 当前迭代的CLOSURE [[左1, [右1], 点位置1], [左2, [右2], 点位置2]]
        # 4.19更新：LR1：[[左1, [右1], 点位置1, [终结符1]], [左2, [右2], 点位置2, [终结符2]]]
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
                for gk, gv in grammar.items():
                    if gk[1] == to_find:
                        if gv[0] == ['$']:
                            continue
                        if (syntax_type == 1 or syntax_type == 2) and [to_find, gv[0], 0] not in ret:
                            ret.append([to_find, gv[0], 0])
                        elif syntax_type == 3:
                            alphas = it[3]
                            beta = rights[point + 1: len(rights)]
                            tmp_vt = []
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
            closure[cnt] = get_CLOSURE_I(closure[cnt])
            len2 = len(closure[cnt])

            if len2 > len1:
                f = 1

    def check(cur_count):
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
        # print(curr, count)
        # 用该项集的初始内容构造项集
        if curr == 0:
            get_closure(curr)
        # 现在编号为curr的项集完整了
        # 接下来对于点右边每个符号进行GO
        # 不同符号分组 {'E': [[左, [右], 位置], [左, [右], 位置]]}
        to_deal = {}
        for each in closure[curr]:
            left, rights, point = each[0], each[1], each[2]
            if syntax_type == 3:
                vts = each[3]
            # 点右边没符号了
            if point == len(rights):
                # TODO:这里处理方式还没想好
                if left == start:
                    go[(curr, '#')] = -2
                else:
                    go[(curr, '#')] = -1
            else:
                # 点右边的符号
                to_move = rights[point]
                # 传统艺能，蠢写法
                tmp = to_deal.get(to_move).copy() if to_deal.get(to_move) is not None else []
                if syntax_type == 1 or syntax_type == 2:
                    tmp.append([left, rights, point + 1])
                elif syntax_type == 3:
                    tmp.append([left, rights, point + 1, vts])
                to_deal[to_move] = tmp

        # to deal 满了 可以分批送去当作初始项集
        for k, v in to_deal.items():
            closure[count] = v
            get_closure(count)
            self_f = check(count)

            # 是一个新的
            if self_f == -1:
                go[(curr, k)] = count
                count += 1
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

            # 项目A->α·属于Ik，对任何终结符和结束符a ACTION[k, a] == rj
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
            # print(f'ACT:{action}，面临输入：{todeal}')
            # print(f'状态栈：{state_stack}')
            # print(f'符号栈：{ch_stack}')
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
                pass
            # 规约需要：1.改变符号栈 2.弹出状态栈 3.根据新状态栈顶、新符号栈顶、GOTO确定入栈状态
            elif act[0] == 'r':
                rule_num = int(act[1:])
                print(f'{cnt}\t{rule_num}\t{ch_stack_top}#{to_deal}\treduction')
                # 找到该规则对应右部 出现弊端
                left, rights = '', []
                for k, v in grammar.items():
                    if k[0] == rule_num:
                        left, rights = k[1], v[0]
                # 注意符号栈里的是规则右部，需要替换为左部，先弹出右部数量的符号
                # 4.15修改：正确做法 先弹出r长度
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
                pass
            else:
                print(act)
                sys.exit()
