import lex
import common

if __name__ == '__main__':
    with open('./data/input.txt', 'r') as f:
        sql = f.readline()
        sql = common.pre_proc(sql)
        lex.main(sql)

