def fix_issue_6_250(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def undo_fix_6_250(code):
