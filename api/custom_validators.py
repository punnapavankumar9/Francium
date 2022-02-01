def check_empty(s):
    if(s == ""):
        return True
    for i in s:
        if(i != ' '):
            return False
    return True
