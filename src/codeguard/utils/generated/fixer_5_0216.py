def undo_fix_5_216(code):
    return code.replace('\t', '    ')
def fix_issue_5_216(code):
    return code.replace('    ', '\t')
