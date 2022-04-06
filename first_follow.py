# 字典格式形如 {'functionCall'=['AVG', 'MAX']}
Grammar = {}
First = {}
First_str = {}
Follow = {}
Vn = []
Start_flag = 'E'


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
    return First_str[in_str]


def get_follow():
    for vn in Vn:
        Follow[vn] = []

    Follow[Start_flag] = ['$']
    f = 1
    while f:
        f = 0
        # 对于每个终结符vn 比如要找G的
        for vn in Vn:
            len1 = len(Follow[vn])
            # 在每个Grammar里找 形如 {'functionCall'=['AVG G', 'MAX']}
            for k, v in Grammar.items():
                # 对functionCall -> 'AVG G'
                for each in v:
                    # functionCall -> ['AVG','G']
                    each = each.split(' ')
                    ff = 0 # 假设 k -> G a A... 求 vn
                    for i, s in enumerate(each):
                        # AVG不是该vn
                        if s != vn:
                            if ff == 0:
                                continue
                            # 当ff==1
                            else:
                                # s 是 GA 的 A 将First(A)除ε加入follow
                                if s in Vn:
                                    # 我觉得不存在First==None的情况
                                    tmp1 = First.get(s).copy()
                                    if '$' in tmp1:
                                        tmp1.remove('$')
                                    tmp2 = Follow.get(vn) if Follow.get(vn) is not None else []
                                    tmp = list(set(tmp1 + tmp2))
                                    Follow[vn] = tmp
                                    ff = 0

                                # s 是 Ga 的 a 直接加入G(vn)的follow中
                                else:
                                    tmp = Follow.get(vn).copy() if Follow.get(vn) is not None else []
                                    if s not in tmp:
                                        tmp.append(s)
                                    Follow[vn] = tmp
                                    ff = 0
                        # 遇到该vn
                        elif s == vn:
                            # 最后遇到 将Follow(k)中的全部内容加到Follow(vn)
                            if i == len(each) - 1:
                                tmp1 = Follow.get(k).copy() if Follow.get(k) is not None else []
                                tmp2 = Follow.get(vn).copy() if Follow.get(vn) is not None else []
                                tmp = list(set(tmp1 + tmp2))
                                Follow[vn] = tmp
                                pass
                            # 不是最后一个 要处理下一个
                            else:
                                ff = 1
            len2 = len(Follow[vn])
            if len1 != len2:
                f = 1
    pass


def main():
    # get_grammar()
    get_first()
    print(First)
    get_follow()
    print(Follow)
    # with open('./data/first.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(First))


main()
