from common import *
from first_follow import get_str_first

# 预测分析表 {[A,a]:[A,α]}
#         a非终结符 α产生式右端
# Grammar_v2 = {}
# M = {}


'''
构造预测分析表
1.从原Grammar中重新提取 {(左端, 序号): ['右端串(右端1 右端2 右端3)']
2.遍历每个产生式，求右端【串】的First集
3.遍历First集，遇到终结符，{(左端, 终结符): [左端，右端串，序号]}
4.若First集中有ε，求左端Follow集
5.遍历Follow集，遇到终结符，{(左端，终结符): [左端，右端串，序号]}
'''


# Grammar形如 'dottedId': ['. uid', '$']
# First,Follow形如 'unionType': ['$', 'ALL', 'DISTINCT']
def get_M():
    # 对文法G的每个产生式A->α k:(左端，序号) v:右端串
    for k, v in Grammar_v2.items():
        first_right = get_str_first(v, First, Vn)
        for each in first_right:
            # 遇到终结符
            if each not in Vn and each != '$':
                M[(k[0], each)] = [k[0], v, k[1]]
            # 遇到ε 求左端Follow
            if each == '$':
                right_follow = Follow[k[0]]
                for each2 in right_follow:
                    # 对Follow中的每个终结符
                    if each2 not in Vn and each2 != '$':
                        M[(k[0], each2)] = [k[0], v, k[1]]
                        # ε同时在follow和first中
                        if each2 == '#':
                            M[(k[0], '#')] = [k[0], v, k[1]]


def main():
    get_M()
