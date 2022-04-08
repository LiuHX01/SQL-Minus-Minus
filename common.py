Grammar = {}
Token = []
First = {}
First_str = {}
Follow = {}
Vn = []
M = {}
Grammar_v2 = {}
Start_flag = 'root'

def pre_proc(in_str):
    in_str = in_str.strip()
    in_str = in_str.split()
    out_str = ''
    for i in in_str:
        if i != '':
            i.strip()
            out_str = out_str + i + ' '
    out_str = ' ' + out_str
    return out_str