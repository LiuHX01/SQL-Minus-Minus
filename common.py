Grammar = {}
First = {}
First_str = {}
Follow = {}
Vn = []
M = {}
Grammar_v2 = {}
Start_flag = 'root'


# 避免输入的字符串不规范
def formatting(in_str):
    if ';' in in_str:
        in_str = in_str.remove(';')
    in_str = in_str.strip()
    in_str = in_str.split()
    out_str = ''
    for i in in_str:
        out_str = out_str + i + ' '
    return out_str
