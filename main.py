import lex
from common import *
import first_follow
import analysis_table
import final



if __name__ == '__main__':
    with open('./data/input.txt', 'r', encoding='utf-8') as f:
        sql = f.readline()
        if sql[-1] == ';':
            sql = sql.replace(';', '')
        sql = pre_proc(sql)
        Token = lex.main(sql)

    for i in Token:
        if 'GROUP BY' in i[0]:
            i[0] = i[0].replace('GROUP BY', 'GROUPBY')
        if 'ORDER BY' in i[0]:
            i[0] = i[0].replace('ORDER BY', 'ORDERBY')
    first_follow.main()
    analysis_table.main()
    # print(Token)
    print('[[[M]]]')
    print(M)
    print(Token)
    final.main(Token, M)

    print('圆满完成')