def pre_proc(in_str):
    in_str = in_str.strip()
    in_str = in_str.split()
    str = ''
    for i in in_str:
        if i != '':
            i.strip()
            str = str + i + ' '
    str = ' ' + str
    return str