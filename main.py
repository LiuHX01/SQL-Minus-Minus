import lex
import common
import first_follow
import analysis_table
import final

Token = []
First = {}
Follow = {}
Vn = []
M = {}
Grammar_2 = {}

if __name__ == '__main__':
    with open('./data/input.txt', 'r', encoding='utf-8') as f:
        sql = f.readline()
        sql = common.pre_proc(sql)
        Token = lex.main(sql)

    for i in Token:
        if 'GROUP BY' in i[0]:
            i[0] = i[0].replace('GROUP BY', 'GROUPBY')
        if 'ORDER BY' in i[0]:
            i[0] = i[0].replace('ORDER BY', 'ORDERBY')
    Vn, Grammar, First, Follow = first_follow.main()
    Grammar_2, M = analysis_table.main(Vn, Follow)
    # print(Token)
    print('[[[M]]]')
    print(M)

    final.main(Token, M)

    print('圆满完成')