def fix_issue_21_1039(code):
    return code.replace('\t', '    ')
def undo_fix_21_1039(code):
    return code.replace('    ', '\t')
