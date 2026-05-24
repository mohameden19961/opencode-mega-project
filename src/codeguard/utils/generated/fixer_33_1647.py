def fix_issue_33_1647(code):
    return code.replace('\t', '    ')
def undo_fix_33_1647(code):
    return code.replace('    ', '\t')
