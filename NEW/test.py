import functions

if __name__ == '__main__':
    LL1, LR0, SLR, LR1 = 0, 1, 2, 3
    path = '../data/grammar.txt'
    syntax_type = LL1

    grammar, vn, vt = functions.get_grammar(path, syntax_type)
    first = functions.get_first(grammar, vn, vt, syntax_type)
    follow = functions.get_follow(grammar, vn, first, syntax_type)

    print(follow)
    pass
