def undo_fix_30_1494(code):
    return code.replace('\t', '    ')
def fix_issue_30_1494(code):
    return code.replace('    ', '\t')
