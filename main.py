import lex
import common
import first_follow
import analysis_table

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

    Vn, Grammar, First, Follow = first_follow.main()
    Grammar_2, M = analysis_table.main(Vn, Follow)
    print(M)