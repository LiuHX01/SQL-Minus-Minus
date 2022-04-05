import sys

# Grammar = {'S':['a A B b c d', '$'],
#            'A':['A S d', '$'],
#            'B':['e C', 'S A h', '$'],
#            'C':['S f', 'C g', '$']} # {'root': ['dmlStatement']}
Grammar = {}
First = {} # {'functionCall'=['AVG', 'MAX']}
Vn = []
# Vn = ['S','A','B','C']


def pre_proc(str):
    str = str.partition('.')[2].strip()
    str = str.partition(' -> ')
    return str[0], str[2]


def get_grammar():
    with open('./data/grammar.txt', 'r', encoding='utf-8') as f:
        it = f.readlines()
        for g in it:
            l, r = pre_proc(g)
            # 认为所有在左侧的都是非终结符 其他都是终结符
            if l not in Vn:
                Vn.append(l)
            if Grammar.get(l) is not None:
                Grammar[l].append(r)
            else:
                Grammar[l] = [r]


    # with open('./data/new_grammar.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(grammar))











def get_first():
    f = 1
    # 当没有改变时停止
    while f:
        print(f)
        f = 0
        for left, v_grammar in Grammar.items():
            # 得到 一个映射
            # S->['a A', 'b']
            for each_grammar in v_grammar:
                # S->'a A' S->b
                each_grammar = each_grammar.split(' ')
                # S->['a','A'] S->['b']
                # 对每个单独规则的单独项，如aA的a和A
                for i, g in enumerate(each_grammar):
                    # 非终结符 left->g(S->A)
                    if g in Vn:
                        tmp1 = First.get(left) if First.get(left) is not None else []
                        tmp2 = First.get(g) if First.get(g) is not None else []
                        tmp = tmp1 + tmp2
                        if len(tmp) > 1:
                            tmp = list(set(tmp))
                            tmp.sort()
                        if len(tmp) != len(First[left]):
                            f = 1

                        First[left] = tmp
                        tmp = ''
                        if '$' not in First[g]:
                            break
                    # 终结符或$
                    else:
                        tmp1 = First.get(left) if First.get(left) is not None else []
                        tmp2 = [g]
                        tmp = tmp1 + tmp2
                        if len(tmp) > 1:
                            tmp = list(set(tmp))
                            tmp.sort()
                        if len(tmp) != len(First[left]):
                            f = 1
                        First[left] = tmp
                        tmp = ''
                        break


    pass



















def main():
    get_grammar()
    for vn in Vn:
        First[vn] = []
    get_first()
    print(First)


main()