import sys
import functions


def get_pred_anal_table(grammar: dict, first: dict, follow: dict, vt: list):
    """预测分析表，这里必是LL(1)

    :param first: {l: ['r1', 'r2', 'r3', '$']}
    :param grammar: {(seq_num, l): ['r1', 'r2', 'r3']}
    :param follow: {l: ['r1', 'r2', 'r3', '#']}
    :param vt: ['vt1', 'vt2']
    :return: pred_anal_table: {(l, vn): [['r1', 'r2', 'r3'], seq_num]}
    """
    pred_anal_table = {}

    for gk, gv in grammar.items():
        seq_num, left = gk[0], gk[1]

        l_right_first = functions.get_str_first(gv, first)
        for each in l_right_first:
            # 对于first(α)中的每个终结符a，令(A, a): [α, num]
            if each in vt:
                pred_anal_table[(left, each)] = [gv, seq_num]
            # 如果$在first(α)中
            elif each == '$':
                right_follow = follow[left]
                # 那么对于follow(A)中的每个终结符b，令(A, b): [α, num]
                for r in right_follow:
                    if r in vt:
                        pred_anal_table[(left, r)] = [gv, seq_num]
                # 且#在follow(A)中，令(A, #): [α, num]
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

    # 对每一个[str, type]对
    for in_str, in_type in token:
        if in_str == 'GROUP BY':
            in_str = 'GROUPBY'
        elif in_str == 'ORDER BY':
            in_str = 'ORDERBY'
        if in_type == 'STR':
            in_type = 'STRING'

        todeal = in_str if in_type == 'KW' or in_type == 'OP' or in_type == 'SE' else in_type

        continue_f = 1
        while continue_f:

            stack_top = stack.pop()
            # 不相等，说明要规约
            if stack_top != todeal:
                try:
                    # 得到表项，得不到就是error
                    rule_num = pred_anal_table[(stack_top, todeal)][1]
                    l_right = pred_anal_table[(stack_top, todeal)][0]
                    o_vn = todeal if todeal != '#' else '#'
                    if todeal == 'GROUPBY':
                        o_vn = 'GROUP BY'
                    if todeal == 'ORDERBY':
                        o_vn = 'ORDER BY'
                except KeyError:
                    print('ERROR: 栈顶不匹配')
                    print(stack_top, todeal)
                    sys.exit()

                # 右端为空，不涉及入栈之类操作
                if l_right == ['$']:
                    print(f'{step}\t{rule_num}\t{stack_top}#{o_vn}\treduction')
                    step += 1
                    continue

                # 倒序入栈
                for each in reversed(l_right):
                    stack.append(each)

                print(f'{step}\t{rule_num}\t{stack_top}#{o_vn}\treduction')
                step += 1

            # 栈顶等于待处理，可以消了
            else:
                # 栈底遇到token尾，规约结束
                if stack_top == todeal == '#':
                    print(f'{step}\t/\t#\taccept')
                    # print(f'{step}\t/\t{stack_top}#{todeal}\taccept')
                    stack = ['#', start]
                    break

                o_vn = todeal if todeal != '#' else '#'
                if todeal == 'GROUPBY':
                    o_vn = 'GROUP BY'
                if todeal == 'ORDERBY':
                    o_vn = 'ORDER BY'
                print(f'{step}\t/\t{stack_top}#{o_vn}\tmove')
                step += 1
                continue_f = 0
