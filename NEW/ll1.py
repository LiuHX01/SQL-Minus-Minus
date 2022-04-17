import sys

import functions


def get_pred_anal_table(grammar: dict, first: dict, follow: dict, vt: list):
    """预测分析表，这里必是LL(1)

    :param first:
    :param grammar: {(seq_num, l): ['r1', 'r2', 'r3']}
    :param follow:
    :param vt:
    :return: pred_anal_table: {(l, vn): [['r1', 'r2', 'r3'], seq_num]}
    """
    pred_anal_table = {}

    for gk, gv in grammar.items():
        seq_num, left = gk[0], gk[1]

        l_right_first = functions.get_str_first(gv, first)
        for each in l_right_first:
            if each in vt:
                pred_anal_table[(left, each)] = [gv, seq_num]
            elif each == '$':
                right_follow = follow[left]
                for r in right_follow:
                    if r in vt:
                        pred_anal_table[(left, r)] = [gv, seq_num]
                if '#' in right_follow:
                    pred_anal_table[(left, '#')] = [gv, seq_num]

    return pred_anal_table


def reduce(token: list, pred_anal_table: dict, start: str):
    """TODO：等待优化写法

    :param start: 'root'
    :param token: [['SELECT', 'KW'], ['t', 'IDN']]
    :param pred_anal_table: {(l, vn): [['r1', 'r2', 'r3'], seq_num]}
    :return: return nothing
    """
    stack = ['#', start]
    step = 1
    token.append(['#', '#'])

    for in_str, in_type in token:
        if in_type == 'KW' or in_type == 'OP' or in_type == 'SE':
            todeal = in_str
        else:
            # 文法已解决STR
            todeal = in_type

        continue_f = 1
        while continue_f:

            stack_top = stack.pop()
            if stack_top != todeal:
                try:
                    rule_num = pred_anal_table[(stack_top, todeal)][1]
                    o_vn = todeal
                    if todeal == 'GROUPBY':
                        o_vn = 'GROUP BY'
                    if todeal == 'ORDERBY':
                        o_vn = 'ORDER BY'
                except KeyError:
                    print('ERROR: 栈顶不匹配')
                    sys.exit()

                l_right = pred_anal_table[(stack_top, todeal)][0]
                if l_right == ['$']:
                    print(f'{step}\t{rule_num}\t{stack_top}#{o_vn}\treduction')
                    step += 1
                    continue

                for each in reversed(l_right):
                    stack.append(each)

                print(f'{step}\t{rule_num}\t{stack_top}#{o_vn}\treduction')
                step += 1

            else:
                if stack_top == todeal == '#':
                    print(f'{step}\t/\t{stack_top}#{todeal}\taccept')
                    break
                o_vn = todeal
                if todeal == 'GROUPBY':
                    o_vn = 'GROUP BY'
                if todeal == 'ORDERBY':
                    o_vn = 'ORDER BY'
                print(f'{step}\t/\t{stack_top}#{o_vn}\tmove')
                step += 1

                continue_f = 0
