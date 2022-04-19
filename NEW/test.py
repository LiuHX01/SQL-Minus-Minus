import functions
import ll1
import lr
import lexer

if __name__ == '__main__':
    sql = 'SELECT t.a FROM t WHERE t.c > 2.0'
    token = lexer.main(sql)
    # token = [['id', 'id'], ['*', '*'], ['id', 'id'], ['+', '+'], ['id', 'id']]
    LL1, LR0, SLR, LR1 = 0, 1, 2, 3
    path = '../data/grammar.txt'
    syntax_type = SLR

    grammar, vn, vt, start = functions.get_grammar(path, syntax_type)
    first = functions.get_first(grammar, vn, vt, syntax_type)
    follow = functions.get_follow(grammar, vn, first, syntax_type)

    if syntax_type == LL1:
        pred = ll1.get_pred_anal_table(grammar, first, follow, vt)
        ll1.reduce(token, pred, start)
    elif syntax_type == LR0 or syntax_type == SLR:
        closure, go = lr.get_fa(grammar, syntax_type, start)
        action, goto = lr.get_pred_anal_table(grammar, follow, closure, go, vn, vt, start, syntax_type)
        for k, v in closure.items():
            print(k, v)
        # for kk, vv in action.items():
        #     print(kk, vv)
        # for kkk, vvv in goto.items():
        #     print(kkk, vvv)
        # print(len(action))
        lr.reduce(token, grammar, action, goto)

