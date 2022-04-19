from common import *


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
                        # 是一连串非终结符 则中间的去掉空 结尾的保留空
                        if '$' in tmp2:
                            # 如果所有的First都有ε
                            if i != len(each_grammar) - 1:
                                tmp2.remove('$')
                        tmp = tmp1 + tmp2

                        tmp = list(set(tmp))

                        First[left] = tmp
                        if '$' not in First.get(g):
                            break
                    # 终结符或$ 直接加入并结束
                    else:
                        tmp1 = First.get(left) if First.get(left) is not None else []
                        tmp2 = [g]
                        tmp = tmp1 + tmp2

                        tmp = list(set(tmp))

                        First[left] = tmp
                        break

            # 操作前后长度对比，因为只可能往里加
            len2 = len(First.get(left))
            if len1 < len2:
                f = 1


# 求一个串的first
# input:形如'AA BB CC'
# return ['a','$']
# 作为一个常用函数，尽量让其只依赖输入参数，便于测试
def get_str_first(in_str, First, Vn):
    l_str = in_str.split(' ')  # ['Cc']
    for i, each in enumerate(l_str):
        # 在这里处理一下终结符的First集
        if each not in Vn:
            First[each] = [each]
        tmp1 = First_str.get(in_str).copy() if First_str.get(in_str) is not None else []
        tmp2 = First.get(each).copy()
        if '$' in tmp2:
            if i != len(l_str) - 1:
                tmp2.remove('$')
        tmp = tmp1 + tmp2
        if len(tmp) > 1:
            tmp = list(set(tmp))
        First_str[in_str] = tmp
        if '$' not in First.get(each):
            break
    return First_str.get(in_str)


# 这里不区分ε和#了，统一用$代替，暂时没什么问题
# 4.11 区分# 更贴合书上 但是没区别
def get_follow():
    for vn in Vn:
        Follow[vn] = []

    Follow[Start_flag] = ['#']
    f = 1
    while f:
        f = 0
        # 对于每个终结符vn 比如要找G的
        for vn in Vn:
            len1 = len(Follow.get(vn))
            # 在每个Grammar里找 形如 {'functionCall'=['AVG G', 'MAX']}
            for k, v in Grammar.items():
                # 对functionCall -> 'AVG G'
                for each in v:
                    # functionCall -> ['AVG','G']
                    each = each.split(' ')
                    ff = 0  # 假设 k -> G a A... 求 vn
                    for i, s in enumerate(each):
                        # AVG不是该vn
                        if s != vn:
                            if ff == 0:
                                continue
                            # 当ff==1 也就是前一个是所求vn
                            else:
                                # cnmd β是到最后的长串
                                # 先将后面的First去ε加入follow
                                long_s = ''
                                for j in range(i, len(each)):
                                    long_s += each[j]
                                    if j != len(each) - 1:
                                        long_s += ' '
                                get_str_first(long_s, First, Vn)
                                tmp1 = First_str.get(long_s).copy()  # if First_str.get(long_s) is not None else []
                                # 不是None 最多是[]
                                tmp2 = Follow.get(vn)
                                if '$' in tmp1:
                                    tmp1.remove('$')
                                    # 将follow(左)加入follow(vn)
                                    tmp3 = Follow.get(k)
                                    tmp2 += tmp3
                                tmp2 = list(set(tmp2 + tmp1))
                                Follow[vn] = tmp2
                                ff = 0

                        # 遇到该vn
                        elif s == vn:
                            # 最后遇到 将Follow(k)中的全部内容加到Follow(vn)
                            if i == len(each) - 1:
                                tmp1 = Follow.get(k).copy() if Follow.get(k) is not None else []
                                tmp2 = Follow.get(vn).copy() if Follow.get(vn) is not None else []
                                tmp = list(set(tmp1 + tmp2))
                                Follow[vn] = tmp
                            # 不是最后一个 要处理下一个
                            else:
                                ff = 1
            len2 = len(Follow.get(vn))
            if len1 < len2:
                f = 1


def main():
    get_first()
    get_follow()
