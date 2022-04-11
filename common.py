Grammar = {}
First = {}
First_str = {}
Follow = {}
Vn = []
M = {}
Grammar_v2 = {}
Start_flag = 'root'


# 避免输入的字符串不规范
def formatting(in_str):
    if ';' in in_str:
        in_str = in_str.replace(';', '')
    in_str = in_str.strip()
    in_str = in_str.split()
    out_str = ''
    for i in in_str:
        out_str = out_str + i + ' '
    return out_str


def get_grammar():
    with open('./data/grammar.txt', 'r', encoding='utf-8') as f:
        it = f.readlines()
        for i, g in enumerate(it):
            if g[0] == '/':
                continue
            g = g.partition('.')[2].strip().partition(' -> ')
            l, r = g[0], g[2]
            if 'GROUP BY' in r:
                r = r.replace('GROUP BY', 'GROUPBY')
            if 'ORDER BY' in r:
                r = r.replace('ORDER BY', 'ORDERBY')
            # 认为所有在左侧的都是非终结符 其他都是终结符
            if l not in Vn:
                Vn.append(l)
            if Grammar.get(l) is not None:
                Grammar[l].append(r)
            else:
                Grammar[l] = [r]
    return Grammar


# 为什么要再提取一次呢？之前的提取没有编号，而且将左端相同的多条规则合并，这里不适用
# 如果有时间会考虑修改，只提取一次
def get_grammar_v2():
    with open('data/grammar.txt', 'r', encoding='utf-8') as f:
        for g in f.readlines():
            # 跳过注释
            if g[0] == '/':
                continue
            tmp1 = g.partition('.')
            # 获得序号
            seqnum = int(tmp1[0])
            tmp2 = tmp1[2].strip().partition(' -> ')
            left = tmp2[0]
            right = tmp2[2]
            # 我真服了 这个GROUP BY和ORDER BY
            if 'GROUP BY' in right:
                right = right.replace('GROUP BY', 'GROUPBY')
            if 'ORDER BY' in right:
                right = right.replace('ORDER BY', 'ORDERBY')
            Grammar_v2[(left, seqnum)] = right

    return Grammar_v2
