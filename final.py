import sys
from common import *


# M形如
# ('selectStatement', 'SELECT'): ['selectStatement', 'querySpecification unionStatements', '6']
def reduce(Token, stack):
    cnt = 1
    # 对于Token中每个
    # print(stack)
    for i, [in_str, in_type] in enumerate(Token):
        # print(in_str, in_type)
        # 关键字、运算符、界符，输入符号是本身
        # todeal = ''
        if in_type == 'KW' or in_type == 'OP' or in_type == 'SE':
            todeal = in_str
        # 否则以类型代替
        else:
            # 能不能统一嗷
            todeal = in_type
            if in_type == 'STR':
                todeal = 'STRING'

        state = ''
        while state != 'move':
            # print(stack)
            stack_top = stack.pop()
            # 不相等 说明还得规约
            if stack_top != todeal:
                state = 'reduction'
                # 得到['selectStatement', 'querySpecification unionStatements', '6']
                try:
                    tmp_list = M[(stack_top, todeal)]
                    rule_num = tmp_list[2]
                    todeal2 = todeal
                    if todeal == 'GROUPBY':
                        todeal2 = 'GROUP BY'
                    if todeal == 'ORDERBY':
                        todeal2 = 'ORDER BY'
                except:
                    print(f'ERROR:不匹配，栈顶:{stack_top}   终结符:{todeal}')
                    print(f'栈:{stack}')
                    sys.exit()

                # 修改了实现和输出方式 其实一样
                if tmp_list[1] == '$':
                    print(f'{cnt}\t{rule_num}\t{stack_top}#{todeal2}\treduction')
                    cnt += 1
                    continue
                right_str_list = tmp_list[1].split(' ')
                # 先入栈
                for each in reversed(right_str_list):
                    # if each != '$':
                    stack.append(each)

                print(f'{cnt}\t{rule_num}\t{stack_top}#{todeal2}\t{state}')
                cnt += 1
            # 相等了 可以规约了
            else:
                if stack_top == todeal == '#':
                    print(f'{cnt}\t/\t{stack_top}#{todeal}\taccept')
                    break
                state = 'move'
                todeal2 = todeal
                if todeal == 'GROUPBY':
                    todeal2 = 'GROUP BY'
                if todeal == 'ORDERBY':
                    todeal2 = 'ORDER BY'
                print(f'{cnt}\t/\t{stack_top}#{todeal2}\t{state}')
                cnt += 1


def main(Token):
    Token.append(['#', '#'])
    stack = ['#', Start_flag]
    reduce(Token, stack)
