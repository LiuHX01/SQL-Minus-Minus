import lex
import common
import first_follow

Token = []
First = {}
Follow = {}
Vn = []

if __name__ == '__main__':
    with open('./data/input.txt', 'r', encoding='utf-8') as f:
        sql = f.readline()
        sql = common.pre_proc(sql)
        Token = lex.main(sql)

    Vn, Grammar, First, Follow = first_follow.main()
