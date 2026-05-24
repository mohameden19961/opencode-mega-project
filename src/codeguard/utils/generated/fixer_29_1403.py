def undo_fix_29_1403(code):
def fix_issue_29_1403(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
