import functions
import ll1
import lr
import lexer

if __name__ == '__main__':
    with open('../data/input.txt', 'r', encoding='utf-8') as f:
        sqls = f.read().splitlines()

    LL1, LR0, SLR, LR1 = 0, 1, 2, 3
    path = '../data/grammar.txt'
    # path = '../data/test_grammar.txt'

    syntax_type = LL1

    grammar, vn, vt, start = functions.get_grammar(path, syntax_type)
    first = functions.get_first(grammar, vn, vt, syntax_type)
    follow = functions.get_follow(grammar, vn, first, syntax_type)

    for sql in sqls:
        if sql == '':
            continue

        token = lexer.main(sql)
        # token = [['i', 'i'], ['*', '*'], ['i', 'i'], ['+', '+'], ['i', 'i']]

        if syntax_type == LL1:
            pred = ll1.get_pred_anal_table(grammar, first, follow, vt)
            ll1.reduce(token, pred, start)
        else:
            closure, go = lr.get_fa(grammar, first, syntax_type, start)
            action, goto = lr.get_pred_anal_table(grammar, follow, closure, go, vn, vt, start, syntax_type)
            lr.reduce(token, grammar, action, goto)
        # break
