# list 模拟栈
import sys

stack = ['root']

# M形如
# ('selectStatement', 'SELECT'): ['selectStatement', 'querySpecification unionStatements', '6']
def reduce(Token, M):
    f = 1
    cnt = 1
    while f:
        f = 0
        # 对于Token中每个
        for i, [in_str, in_type] in enumerate(Token):
            # 是关键字、运算符、界符，输入符号是本身
            todeal = ''
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
                    except:
                        print(f'ERROR:不匹配，栈顶:{stack_top}   终结符:{todeal}')
                        sys.exit()
                    # 先入栈
                    right_str_list = tmp_list[1].split(' ')
                    for each in reversed(right_str_list):
                        if each != '$':
                            stack.append(each)

                    rule_num = tmp_list[2]
                    todeal2 = todeal
                    if todeal == 'GROUPBY':
                        todeal2 = 'GROUP BY'
                    if todeal == 'ORDERBY':
                        todeal2 = 'ORDER BY'
                    print(f'{cnt}\t{rule_num}\t{stack_top}#{todeal2}\t{state}')
                    cnt += 1
                # 相等了 可以规约了
                else:
                    state = 'move'
                    todeal2 = todeal
                    if todeal == 'GROUPBY':
                        todeal2 = 'GROUP BY'
                    if todeal == 'ORDERBY':
                        todeal2 = 'ORDER BY'
                    print(f'{cnt}\t/\t{stack_top}#{todeal2}\t{state}')
                    cnt += 1
        pass
    pass


def main(Token, M):
    reduce(Token, M)