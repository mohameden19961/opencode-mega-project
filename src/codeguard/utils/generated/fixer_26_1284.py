def undo_fix_26_1284(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
def fix_issue_26_1284(code):
