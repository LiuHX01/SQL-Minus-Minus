import lex
from common import *
import first_follow
import analysis_table
import final





if __name__ == '__main__':
    with open('./data/input.txt', 'r', encoding='utf-8') as f:
        sql = f.readline()
    sql = formatting(sql)

    # 等待一个新的Lexical analyzer
    Token = lex.main(sql)

    # 原因用空格连接两个符号
    for i in Token:
        if 'GROUP BY' in i[0]:
            i[0] = i[0].replace('GROUP BY', 'GROUPBY')
        if 'ORDER BY' in i[0]:
            i[0] = i[0].replace('ORDER BY', 'ORDERBY')

    # 得到该文法的FIRST FOLLOW集
    first_follow.main()

    # 构造预测分析表
    analysis_table.main()

    # 进行最终规约
    final.reduce(Token)

    print('Done!')