def fix_issue_20_983(code):
    return code.replace('\t', '    ')
def undo_fix_20_983(code):
    return code.replace('    ', '\t')
