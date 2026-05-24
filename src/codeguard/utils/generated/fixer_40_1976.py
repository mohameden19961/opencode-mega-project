def fix_issue_40_1976(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
def undo_fix_40_1976(code):
