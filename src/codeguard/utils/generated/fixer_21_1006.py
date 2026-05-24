def fix_issue_21_1006(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
def undo_fix_21_1006(code):
