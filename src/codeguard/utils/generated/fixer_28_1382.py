def undo_fix_28_1382(code):
def fix_issue_28_1382(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
