# 字典格式形如 {'functionCall'=['AVG', 'MAX']}
Grammar = {}
First = {}
First_str = {}
Vn = []
Start_flag = 'root'


# 两个测试用例 结果都对 怀疑指导书上例子错了
# Grammar = {'A':['B C c','g D B'],
#            'B':['b C D E', '$'],
#            'C':['D a B','c a'],
#            'D':['d D', '$'],
#            'E':['g A f','c']} # {'root': ['dmlStatement']}
Grammar = {
    'E':['T EE'],
    'EE':['+ T EE', '$'],
    'T':['F TT'],
    'TT':['* F TT', '$'],
    'F':['( E )','i']
}
Vn = ['E','EE','T','TT','F']


def pre_proc(in_str):
    in_str = in_str.partition('.')[2].strip()
    in_str = in_str.partition(' -> ')
    return in_str[0], in_str[2]


def get_grammar():
    with open('./data/grammar.txt', 'r', encoding='utf-8') as f:
        it = f.readlines()
        for g in it:
            if g[0] == '/':
                continue
            l, r = pre_proc(g)
            # 认为所有在左侧的都是非终结符 其他都是终结符
            if l not in Vn:
                Vn.append(l)
            if Grammar.get(l) is not None:
                Grammar[l].append(r)
            else:
                Grammar[l] = [r]

    # with open('./data/new_grammar.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(Grammar))


def get_first():
    for vn in Vn:
        First[vn] = []

    f = 1
    # 当没有改变时停止
    while f:
        f = 0
        for left, v_grammar in Grammar.items():
            len1 = len(First.get(left))
            # 得到 每一个映射
            # S->['a A', 'b']
            for each_grammar in v_grammar:
                # S->'a A'
                each_grammar = each_grammar.split(' ')
                # S->['a','A']
                # 对每个单独规则的单独项，如aA的a和A
                for i, g in enumerate(each_grammar):
                    # 非终结符 left->g(S->A)
                    if g in Vn:
                        tmp1 = First.get(left) if First.get(left) is not None else []
                        tmp2 = First.get(g).copy() if First.get(g) is not None else []
                        # 是一连串非终极符 则中间的去掉空 结尾的保留空
                        if '$' in tmp2:
                            if i != len(each_grammar) - 1:
                                tmp2.remove('$')
                        tmp = tmp1 + tmp2

                        if len(tmp) > 1:
                            tmp = list(set(tmp))

                        First[left] = tmp
                        if '$' not in First[g]:
                            break
                    # 终结符或$ 直接加入并结束
                    else:
                        tmp1 = First.get(left) if First.get(left) is not None else []
                        tmp2 = [g]
                        tmp = tmp1 + tmp2

                        if len(tmp) > 1:
                            tmp = list(set(tmp))

                        First[left] = tmp
                        break

            # 操作前后长度对比，因为只可能往里加
            len2 = len(First.get(left))
            if len1 != len2:
                f = 1


# 求一个串的first
# input:形如'AA BB CC'
def get_str_first(in_str):
    res = []
    l_str = in_str.split(' ')
    for i, each in enumerate(l_str):
        # 在这里处理一下终结符的First集
        if each not in Vn:
            First[each] = [each]
        tmp1 = First_str.get(in_str).copy() if First_str.get(in_str) is not None else []
        tmp2 = First[each].copy()
        if '$' in tmp2:
            if i != len(l_str) - 1:
                tmp2.remove('$')
        tmp = tmp1 + tmp2
        if len(tmp) > 1:
            tmp = list(set(tmp))
        First_str[in_str] = tmp
        if '$' not in First[each]:
            break



def main():
    # get_grammar()
    get_first()
    print(First)
    get_str_first('EE E')
    print(First_str)
    # with open('./data/first.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(First))


main()
