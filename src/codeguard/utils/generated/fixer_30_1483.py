def undo_fix_30_1483(code):
    return code.replace('\t', '    ')
def fix_issue_30_1483(code):
    return code.replace('    ', '\t')
