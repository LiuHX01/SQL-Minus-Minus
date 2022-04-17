import functions
import ll1
import lexer

if __name__ == '__main__':
    sql = 'SELECT t.a FROM t WHERE t.c > 2.0'
    Token = lexer.main(sql)

    LL1, LR0, SLR, LR1 = 0, 1, 2, 3
    path = '../data/grammar.txt'
    syntax_type = LL1

    grammar, vn, vt, start = functions.get_grammar(path, syntax_type)
    first = functions.get_first(grammar, vn, vt, syntax_type)
    follow = functions.get_follow(grammar, vn, first, syntax_type)

    if syntax_type == LL1:
        pred = ll1.get_pred_anal_table(grammar, first, follow, vt)
        ll1.reduce(Token, pred, start)
    else:
        pass
