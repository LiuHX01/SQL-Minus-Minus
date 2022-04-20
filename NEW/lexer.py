import random

# 存储词法分析结果
Token = []

# 关键字字典
keywords = {'SELECT': 1,
            'FROM': 2,
            'WHERE': 3,
            'AS': 4,
            '*': 5,
            'INSERT': 6,
            'INTO': 7,
            'VALUES': 8,
            'VALUE': 9,
            'DEFAULT': 10,
            'UPDATE': 11,
            'SET': 12,
            'DELETE': 13,
            'JOIN': 14,
            'LEFT': 15,
            'RIGHT': 16,
            'ON': 17,
            'MIN': 18,
            'MAX': 19,
            'AVG': 20,
            'SUM': 21,
            'UNION': 22,
            'ALL': 23,
            'GROUP BY': 24,
            'HAVING': 25,
            'DISTINCT': 26,
            'ORDER BY': 27,
            'TRUE': 28,
            'FALSE': 29,
            'UNKNOWN': 30,
            'IS': 31,
            'NULL': 32
            }

# 运算符字典
ops = {'=': 1,
       '>': 2,
       '<': 3,
       '>=': 4,
       '<=': 5,
       '!=': 6,
       '<=>': 7,
       'AND': 8,
       '&&': 9,
       '||': 10,
       'OR': 11,
       'XOR': 12,
       '.': 13,
       '!': 14
       }

# 界符字典
ses = {'(': 1,
       ')': 2,
       ',': 3
       }


class NFA:
    def __init__(self, nfa_states, symbols, nfa_tran_state, nfa_start_state, nfa_final_states):
        self.nfa_states = nfa_states
        self.symbols = symbols
        self.nfa_tran_state = nfa_tran_state
        self.nfa_start_state = nfa_start_state
        self.nfa_final_states = nfa_final_states

    # ε-closure函数
    def closure(self, I):
        for i in I:
            for f in self.nfa_tran_state:
                if f[0] == i and f[1] == "$":  # $表示空字符
                    if f[2] not in I:
                        I.append(f[2])
        return sorted(I)

    # move(I, a)函数
    def move_nfa(self, I, a):
        new_I = []
        for i in I:
            for f in self.nfa_tran_state:
                if f[0] == i and f[1] == a:
                    if f[2] not in new_I:
                        new_I.append(f[2])
        return sorted(new_I)


class DFA:
    def __init__(self, dfa_states, symbols, dfa_tran_state, dfa_start_state, dfa_final_states):
        self.dfa_states = dfa_states
        self.symbols = symbols
        self.dfa_tran_state = dfa_tran_state
        self.dfa_start_state = dfa_start_state
        self.dfa_final_states = dfa_final_states

    def print_dfa(self):
        print(self.dfa_states)
        print(self.symbols)
        print(self.dfa_tran_state)
        print(self.dfa_start_state)
        print(self.dfa_final_states)

    def move_dfa(self, I, a):
        new_I = []
        for i in I:
            for f in self.dfa_tran_state:
                if f[0] == i and f[1] == a:
                    if f[2] not in new_I:
                        new_I.append(f[2])
        # print(sorted(new_I))
        return sorted(new_I)

    # DFA最小化
    def minimize(self):

        total_states = set()
        for state in self.dfa_states:
            total_states.add(self.dfa_states.index(state))
        final_states = set()
        for state in self.dfa_final_states:
            final_states.add(self.dfa_states.index(state))
        not_final_states = total_states - final_states

        P = [final_states, not_final_states]
        W = [final_states, not_final_states]

        def get_source_set(target_set, symbol):
            source_set = set()
            for state in total_states:
                for f in self.dfa_tran_state:
                    if f[0] == state and f[1] == symbol and f[2] in target_set:
                        source_set.add(state)
            return source_set

        while W:
            A = random.choice(W)
            W.remove(A)
            for symbol in self.symbols:
                X = get_source_set(A, symbol)
                P_temp = []
                for Y in P:
                    S = X & Y
                    S1 = Y - X
                    if len(S) and len(S1):
                        P_temp.append(S)
                        P_temp.append(S1)
                        if Y in W:
                            W.remove(Y)
                            W.append(S)
                            W.append(S1)
                        else:
                            if len(S) <= len(S1):
                                W.append(S)
                            else:
                                W.append(S1)
                    else:
                        P_temp.append(Y)
                P = P_temp
        # 得到最后的划分P
        # print(P)
        # 合并等价节点
        for state_set in P:
            state_list = list(state_set)
            if len(state_list) > 1:
                index0 = state_list[0]
                for i, state in enumerate(state_list, 1):
                    index = state
                    self.dfa_states[index] = []  # 由于用下标检索，需要保留空元素
                    if self.dfa_states[index] in self.dfa_final_states:
                        self.dfa_final_states.remove(self.dfa_states[index])
                    for f in self.dfa_tran_state:
                        if f[0] == index: f[0] = index0
                        if f[2] == index: f[2] = index0

        # 去除不可达节点（死状态）
        state_set = set()
        state_set1 = set(self.dfa_start_state)
        states = self.dfa_start_state
        while True:
            for symbol in self.symbols:
                state_set1 = state_set1 | set(self.move_dfa(states, symbol))
            if state_set1 == state_set:
                break
            else:
                state_set = state_set1
                states = list(state_set)
        # print(states)
        for i, state in enumerate(self.dfa_states):
            if i not in states:
                self.dfa_states[i] == []
                if self.dfa_states[i] in self.dfa_final_states:
                    self.dfa_final_states.remove(self.dfa_states[i])
                for f in self.dfa_tran_state:
                    if f[0] == i or f[2] == i:
                        self.dfa_tran_state.remove(f)

    def read_string(self, input_str):
        for c in input_str:
            if c not in self.symbols:
                print('illegal str!')
                return
        next_states = self.dfa_start_state
        for c in input_str:
            next_states = self.move_dfa(next_states, c)
            # print(next_states)
        return next_states


# 用于添加状态转换函数
def myappend(fx, k, e, new_k):
    t = []
    t.append(k)
    t.append(e)
    t.append(new_k)
    fx.append(t)


# 检索对应NFA的终态
def check_final_type(final_state, nfa=NFA):
    for i in nfa.nfa_final_states:
        if i in final_state:
            return i
    return -1


# 判断新生成的子集是否已经存在，若存在返回位置，否则返回-1
def is_inDFA(new_k, states):
    new_set = set(new_k)
    index = 0
    for k in states:
        old_set = set(k)
        if old_set == new_set:
            return index
        index = index + 1
    return -1


# 判断DFA状态是否为终态
def is_final(new_k, states):
    new_k_set = set(new_k)
    states_set = set(states)
    result = not states_set.isdisjoint(new_k_set)
    return result


# NFA to DFA（NFA的确定化）
def NFA2DFA(nfa=NFA):
    dfa_states = []
    dfa_tran_state = []
    dfa_start_state = [0]
    dfa_final_states = []

    dfa_start_state = nfa.closure(nfa.nfa_start_state)  # DFA的初态
    dfa_states.append(dfa_start_state)
    for k in dfa_states:
        for e in nfa.symbols:
            new_k = nfa.closure(nfa.move_nfa(k, e))
            if new_k:
                if is_inDFA(new_k, dfa_states) == -1:  # 不存在于当前子集中，则加入
                    dfa_states.append(new_k)
                    myappend(dfa_tran_state, is_inDFA(k, dfa_states), e, is_inDFA(new_k, dfa_states))
                else:  # 存在于当前子集中，则不加入
                    myappend(dfa_tran_state, is_inDFA(k, dfa_states), e, is_inDFA(new_k, dfa_states))

    for k in dfa_states:
        if is_final(k, nfa.nfa_final_states):
            dfa_final_states.append(k)

    dfa = DFA(dfa_states, nfa.symbols, dfa_tran_state, dfa_start_state, dfa_final_states)
    return dfa


# 处理输出格式
def deal(in_str):
    # a	<IDN,a>
    tk = in_str.partition('\t')
    Token.append([tk[0], tk[2].rpartition(',')[0][1:]])


def main(sql):
    Token.clear()
    nfa_states = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    symbols = []
    nfa_tran_state = []
    nfa_start_state = [0]
    nfa_final_states = [1, 3, 4, 5, 8]

    all_symbol = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_*=><!&|.(),\"'
    nodigit_symbol = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    normal_symbol = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    digit_symbol = '0123456789'
    hex_symbol = '0123456789ABCDEF'

    # 输入符号集
    for char in all_symbol:
        symbols.append(char)

    # 标识符IDN
    for char in nodigit_symbol:
        myappend(nfa_tran_state, 0, char, 1)
    for char in normal_symbol:
        myappend(nfa_tran_state, 1, char, 1)

    # 属性运算符'.' -> 'IDN.IDN'
    myappend(nfa_tran_state, 1, '.', 2)
    for char in nodigit_symbol:
        myappend(nfa_tran_state, 2, char, 3)
    for char in normal_symbol:
        myappend(nfa_tran_state, 3, char, 3)

    # 十进制整数INT
    for char in digit_symbol:
        myappend(nfa_tran_state, 0, char, 4)
    for char in digit_symbol:
        myappend(nfa_tran_state, 4, char, 4)

    # 浮点数FLOAT
    myappend(nfa_tran_state, 4, '.', 5)
    for char in digit_symbol:
        myappend(nfa_tran_state, 5, char, 5)

    # 十六进制整数INT(HEX)
    myappend(nfa_tran_state, 0, '0', 6)
    myappend(nfa_tran_state, 6, 'x', 7)
    myappend(nfa_tran_state, 6, 'X', 7)
    for char in hex_symbol:
        myappend(nfa_tran_state, 7, char, 8)
    for char in hex_symbol:
        myappend(nfa_tran_state, 8, char, 8)

    nfa = NFA(nfa_states, symbols, nfa_tran_state, nfa_start_state, nfa_final_states)
    dfa = NFA2DFA(nfa)
    dfa.minimize()
    # dfa.print_dfa()

    # sql = 'a>=b,!a!=0,am <=>a <=bm'
    # sql = '0x1111AD 0.1 0.0002'
    print(sql)

    # 处理界符
    sql = sql.replace('(', ' ( ').replace(')', ' ) ').replace(',', ' , ').replace('\"', ' \" ')
    # 处理运算符
    sql = sql.replace('<', ' < ').replace('>', ' > ').replace('=', ' = ').replace('<  =', '<=').replace('>  =',
                                                                                                        '>=').replace(
        '<=  >', '<=>').replace('!', ' ! ').replace('!  =', '!=').replace('&&', ' && ').replace('||', ' || ')

    sqllist = sql.split()
    # # sqllist = [i for i in sqllist if i]
    # print(len(sqllist))
    # print(sqllist)
    flag_kw = 0  # 用于判断GROUP BY 和 ORDER BY
    flag_q = 0  # 用于判断字符串的双引号
    for i, str in enumerate(sqllist):
        if str in keywords:
            print(f'{str}\t<KW,{keywords.get(str)}>')
            deal(f'{str}\t<KW,{keywords.get(str)}>')
        elif (str in ('GROUP', 'ORDER')) and (sqllist[i + 1] == 'BY'):
            str = str + ' BY'
            print(f'{str}\t<KW,{keywords.get(str)}>')
            deal(f'{str}\t<KW,{keywords.get(str)}>')
            flag_kw = 1
        elif str == 'BY' and flag_kw == 1:
            flag_kw = 0
        elif str in ops:
            print(f'{str}\t<OP,{ops.get(str)}>')
            deal(f'{str}\t<OP,{ops.get(str)}>')
        elif flag_q == 1:
            if str == '\"':
                flag_q = 0
        elif str == '\"' and flag_q == 0:
            string_str = ''
            while sqllist[i + 1] != '\"':
                string_str += sqllist[i + 1]
                i += 1
            print(f'{string_str}\t<STR,{string_str}>')
            deal(f'{string_str}\t<STR,{string_str}>')
            flag_q = 1
        elif str in ses:
            print(f'{str}\t<SE,{ses.get(str)}>')
            deal(f'{str}\t<SE,{ses.get(str)}>')
        else:
            final_state_number = dfa.read_string(str)[0]
            final_state = dfa.dfa_states[final_state_number]
            # print(final_state)
            if final_state in dfa.dfa_final_states:
                type = check_final_type(final_state, nfa)
                # print(type)
                if type == 1:
                    print(f'{str}\t<IDN,{str}>')
                    deal(f'{str}\t<IDN,{str}>')
                elif type == 3:
                    strlist = str.split('.')
                    print(f'{strlist[0]}\t<IDN,{strlist[0]}>')
                    deal(f'{strlist[0]}\t<IDN,{strlist[0]}>')
                    print(f'.\t<OP,13>')
                    deal(f'.\t<OP,13>')
                    print(f'{strlist[1]}\t<IDN,{strlist[1]}>')
                    deal(f'{strlist[1]}\t<IDN,{strlist[1]}>')
                elif type in (4, 8):
                    print(f'{str}\t<INT,{str}>')
                    deal(f'{str}\t<INT,{str}>')
                elif type == 5:
                    print(f'{str}\t<FLOAT,{str}>')
                    deal(f'{str}\t<FLOAT,{str}>')
            else:
                print('Wrong!')

    # print(Token)
    return Token