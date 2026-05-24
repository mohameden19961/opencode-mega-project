def undo_fix_28_1385(code):
def fix_issue_28_1385(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
