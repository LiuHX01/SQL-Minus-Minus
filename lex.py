import sys

Token = []

keywords = {'SELECT': 1,
            'FROM': 2,
            'WHERE': 3,
            'AS': 4,
            'INSERT': 5,
            'INTO': 6,
            'VALUES': 7,
            'UPDATE': 8,
            'DELETE': 9,
            'JOIN': 10,
            'LEFT': 11,
            'RIGHT': 12,
            'MIN': 13,
            'MAX': 14,
            'AVG': 15,
            'SUM': 16,
            'UNION': 17,
            'ALL': 18,
            'GROUP BY': 19,
            'HAVING': 20,
            'DISTINCT': 21,
            'ORDER BY': 22,
            'TRUE': 23,
            'FALSE': 24,
            'IS': 25,
            'NOT': 26,
            'NULL': 27
            }

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
       '.': 13
       }
op_sig = ('=', '>', '<', '!', '|', '&')

ses = {'(': 1,
       ')': 2,
       ',': 3
       }


# -------------------------------------------------------------------------------
def deal(in_str):
    # a	<IDN,a>
    tk = in_str.partition('\t')
    Token.append([tk[0], tk[2].rpartition(',')[0][1:]])


# 一些函数
def checkIDN(str):
    if str[0] not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
        print(f'{str}格式错误')
        sys.exit()
        return False
    for c in str:
        if c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
            print(f'{str}中存在非法字符{c}')
            sys.exit()
            return False
    return True


# 十六进制小数？
def checkHEX(str):
    if len(str) < 3:
        return False
    else:
        for i, c in enumerate(str):
            if i == 0 and c != '0':
                return False
            elif (i == 1 and c != 'x') and (i == 1 and c != 'X'):
                return False
            elif i > 1 and c not in '0123456789abcdefABCDEF':
                return False

    return True


def Print(tmp, isStr=False):
    if tmp != '':
        if isStr:
            print(f'{tmp}\t<STR,{tmp}>')
            deal(f'{tmp}\t<STR,{tmp}>')
        elif keywords.get(tmp) is not None:
            print(f'{tmp}\t<KW,{keywords.get(tmp)}>')
            deal(f'{tmp}\t<KW,{keywords.get(tmp)}>')
        elif ops.get(tmp) is not None:
            print(f'{tmp}\t<OP,{ops.get(tmp)}>')
            deal(f'{tmp}\t<OP,{ops.get(tmp)}>')
        elif tmp.isdigit():
            print(f'{tmp}\t<INT,{tmp}>')
            deal(f'{tmp}\t<INT,{tmp}>')
        elif tmp.replace('.', '').isdigit():
            print(f'{tmp}\t<FLOAT,{tmp}>')
            deal(f'{tmp}\t<FLOAT,{tmp}>')
        elif checkHEX(tmp):
            print(f'{tmp}\t<INT,{tmp}>')
            deal(f'{tmp}\t<INT,{tmp}>')
        elif checkIDN(tmp):
            print(f'{tmp}\t<IDN,{tmp}>')
            deal(f'{tmp}\t<IDN,{tmp}>')
        else:
            print('不可能到这的')
            sys.exit()


# -------------------------------------------------------------------------------
def main(str):
    tmp = ''
    isStr = False
    lPair = 0
    for i, c in enumerate(str):
        if c == ' ' and isStr == False:
            if tmp == 'GROUP' or tmp == 'ORDER':
                tmp += c
            else:
                Print(tmp)
                tmp = ''

        # 小数点还是属性符
        elif c == '.' and isStr == False:
            if str[i + 1].isdigit():
                tmp += c
            else:
                print(f'{tmp}\t<IDN,{tmp}>')
                deal(f'{tmp}\t<IDN,{tmp}>')
                print(f'.\t<OP,13>')
                deal(f'.\t<OP,13>')
                tmp = ''

        # 部分连在一起的运算符 除了点
        elif c in op_sig and isStr == False:
            Print(tmp)
            # <=> 在 <
            if str[i - 1] not in op_sig and str[i + 1] in op_sig and str[i + 2] in op_sig:
                tmp = c + str[i + 1] + str[i + 2]
                Print(tmp)
                # print(f'{c + str[i + 1] + str[i + 2]}\t<OP,{ops.get(c + str[i + 1] + str[i + 2])}>')
            # <= 在 <
            elif str[i - 1] not in op_sig and str[i + 1] in op_sig and str[i + 2] not in op_sig:
                tmp = c + str[i + 1]
                Print(tmp)
                # print(f'{c+str[i+1]}\t<OP,{ops.get(c+str[i+1])}>')
            # <=> 在 = 或 >
            elif (str[i - 1] in op_sig and str[i + 1] in op_sig) or (str[i - 1] in op_sig and str[i - 2] in op_sig):
                pass
            # <= 在 =
            elif str[i - 1] in op_sig and str[i + 1] not in op_sig:
                pass
            # < 在 <
            elif str[i - 1] not in op_sig and str[i + 1] not in op_sig:
                tmp = c
                Print(tmp)
                # print(f'{c}\t<OP,{ops.get(c)}>')
            else:
                print('ERROR:没见过这样的运算符啊')
            tmp = ''

        # 左右括号 逗号
        elif (c == '(' or c == ')' or c == ',') and isStr == False:
            Print(tmp)
            if c == '(':
                lPair += 1
                if i == len(str) - 1 and lPair > 0:
                    print('ERROR:括号不匹配')
                    sys.exit()
            elif c == ')':
                if lPair <= 0:
                    print('ERROR:括号不匹配')
                    sys.exit()
                else:
                    lPair -= 1
            print(f'{c}\t<SE,{ses.get(c)}>')
            tmp = ''

        elif c == "'":
            # 左引号
            if isStr == False:
                isStr = True
            # 右引号
            else:
                Print(tmp, isStr=isStr)
                isStr = False
                tmp = ''

        else:
            tmp += c

    return Token
