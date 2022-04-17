def get_grammar(path: str, syntax_type: int):
    """从文档中提取文法并储存，适用不同文法

    :param path: 语法文件路径
    :param syntax_type: 使用文法种类 LL1:0, LR0:1, SRL:2, LR1:3
    :return: LL(1): grammar: {(seq_num, l): ['r1', 'r2', 'r3']}
             not LL(1): grammar: {(seq_num, l): [['r1', 'r2', 'r3'], [0, 1, 2, 3(点前符号数)]]},
             vn: ['vn1', 'vn2'],
             vt: ['vt1', 'vt2'],
             start: 'root~'
    """
    vn, vt, grammar, start = [], [], {}, ''

    with open(path, 'r', encoding='utf-8') as f:
        l_grammar = f.readlines()

    # g形如 6. selectStatement -> querySpecification unionStatements
    for g in l_grammar:
        if g[0] == '/':
            continue

        g = g.partition('.')
        seq_num = int(g[0])
        g = g[2].strip().partition(' -> ')
        left = g[0]

        # 这里要将 GROUP BY 看做一个符号
        l_right = g[2]
        if 'GROUP BY' in l_right:
            l_right = l_right.replace('GROUP BY', 'GROUPBY')
        elif 'ORDER BY' in l_right:
            l_right = l_right.replace('ORDER BY', 'ORDERBY')
        l_right = l_right.split(' ')

        # LL(1)文法
        if syntax_type == 0:
            grammar[(seq_num, left)] = l_right
            if seq_num == 1:
                start = left
        # 非LL(1)文法
        else:
            if seq_num == 1:
                grammar[(0, left + '~')] = [[left], [0, 1]]
                vn.append(left + '~')
                start = left + '~'
            point_pos = [x for x in range(len(l_right) + 1)] if l_right != ['$'] else [-1]
            grammar[(seq_num, left)] = [l_right, point_pos]

        # 认为出现在左端的都是终结符
        if left not in vn:
            vn.append(left)

    # 认为所有只出现在右端且非ε的都是非终结符
    for k, v in grammar.items():
        l_right = v if syntax_type == 0 else v[0]
        for each in l_right:
            if each not in vn and each not in vt and each != '$':
                vt.append(each)

    return grammar, vn, vt, start


def get_first(grammar: dict, vn: list, vt: list, syntax_type: int):
    """

    :param grammar: LL(1): {(seq_num, l): ['r1', 'r2', 'r3']}
                    not LL(1): {(seq_num, l): [['r1', 'r2', 'r3'], [0, 1, 2, 3(点前符号数)]]}
    :param vn: ['vn1', 'vn2']
    :param vt: ['vt1', 'vt2']
    :param syntax_type: 使用文法种类 LL1:0, LR0:1, SRL:2, LR1:3
    :return: first: {l: ['r1', 'r2', 'r3', '$']}
    """
    first = {'$': '$'}
    for each in vn + vt:
        first[each] = [] if each in vn else [each]

    # 迭代，当没有新增时停止
    stop_f = 1
    while stop_f:
        stop_f = 0

        # 对于每个非终结符
        for each in vn:
            len1 = len(first[each])
            # 在每条规则中
            for gk, gv in grammar.items():
                # 该规则左端是此非终结符
                if gk[1] == each:
                    l_right = gv if syntax_type == 0 else gv[0]
                    # 对于该规则右端每一个符号
                    for i, r in enumerate(l_right):
                        if r in vt or r == '$':
                            if r not in first[each]:
                                first[each].append(r)
                            break
                        elif r in vn:
                            # 新写法，避免刷新式写入和许多不知意义的tmp
                            for j in first[r]:
                                if j not in first[each]:
                                    if j == '$' and i == len(l_right) - 1:
                                        first[each].append(j)
                                    elif j != '$':
                                        first[each].append(j)
                        if '$' not in first[r]:
                            break

            len2 = len(first[each])
            if len1 < len2:
                stop_f = 1

    return first


def get_str_first(instr_l: list, first: dict):
    """得到一个串的first集

    :param instr_l: ['h', 'e', 'l', 'l', 'o']
    :param first:
    :return: ['q', 'w', '$']
    """
    ret = []

    # 对于该串的每个字符
    for i, ith_ch in enumerate(instr_l):
        ith_first = first[ith_ch]
        for each in ith_first:
            if each not in ret:
                if each == '$' and i == len(instr_l) - 1:
                    ret.append(each)
                elif each != '$':
                    ret.append(each)
        if '$' not in ith_first:
            break

    return ret


def get_follow(grammar: dict, vn: list, first: dict, syntax_type: int):
    """

    :param grammar: LL(1): {(seq_num, l): ['r1', 'r2', 'r3']}
                    not LL(1): {(seq_num, l): [['r1', 'r2', 'r3'], [0, 1, 2, 3(点前符号数)]]}
    :param vn: ['vn1', 'vn2']
    :param syntax_type: 使用文法种类 LL1:0, LR0:1, SRL:2, LR1:3
    :param first: {l: ['r1', 'r2', 'r3', '$']}
    :return: follow: {l: ['r1', 'r2', 'r3', '#']}
    """
    follow = {}
    for each in vn:
        follow[each] = []

    for k in grammar:
        if (k[0] == 0 and syntax_type != 0) or (k[0] == 1 and syntax_type == 0):
            follow[k[1]].append('#')
            break

    stop_f = 1
    while stop_f:
        stop_f = 0

        for each in vn:
            len1 = len(follow[each])
            for gk, gv in grammar.items():
                l_right = gv if syntax_type == 0 else gv[0]
                proc_f = 0
                for i, r in enumerate(l_right):
                    if r != each:
                        if not proc_f:
                            continue
                        # 该符号的前一个是所求vn
                        else:
                            l_str_first = get_str_first(l_right[i: len(l_right)], first)
                            for j in l_str_first:
                                if j not in follow[each]:
                                    if j != '$':
                                        follow[each].append(j)
                                    else:
                                        for j in follow[gk[1]]:
                                            if j not in follow[each]:
                                                follow[each].append(j)
                            proc_f = 0
                    # 遇到所求vn
                    else:
                        if i == len(l_right) - 1:
                            for j in follow[gk[1]]:
                                if j not in follow[each]:
                                    follow[each].append(j)
                        else:
                            proc_f = 1

            len2 = len(follow[each])
            if len1 < len2:
                stop_f = 1

    return follow
