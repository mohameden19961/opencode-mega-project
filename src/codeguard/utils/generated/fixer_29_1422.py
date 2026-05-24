def fix_issue_29_1422(code):
def undo_fix_29_1422(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
