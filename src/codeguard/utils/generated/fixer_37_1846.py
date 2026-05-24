def fix_issue_37_1846(code):
    return code.replace('    ', '\t')
def undo_fix_37_1846(code):
    return code.replace('\t', '    ')
