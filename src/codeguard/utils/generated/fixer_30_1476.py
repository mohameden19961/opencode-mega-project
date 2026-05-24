def undo_fix_30_1476(code):
    return code.replace('    ', '\t')
def fix_issue_30_1476(code):
    return code.replace('\t', '    ')
