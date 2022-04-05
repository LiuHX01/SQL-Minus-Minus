import lex
import common

if __name__ == '__main__':
    with open('./data/input.txt', 'r', encoding='utf-8') as f:
        sql = f.readline()
        sql = common.pre_proc(sql)
        lex.main(sql)

