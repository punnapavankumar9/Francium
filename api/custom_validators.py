def check_empty(s):
    if(s == ""):
        return True
    for i in s:
        if(i != ' '):
            return False
    return True

def pk_int_validater(s):
    for i in s:
        if(not i.isdigit()):
            return False
    return True