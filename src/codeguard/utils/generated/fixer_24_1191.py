def fix_issue_24_1191(code):
    return code.replace('\t', '    ')
def undo_fix_24_1191(code):
    return code.replace('    ', '\t')
