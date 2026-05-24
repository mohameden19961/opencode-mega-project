def fix_issue_30_1478(code):
    return code.replace('    ', '\t')
def undo_fix_30_1478(code):
    return code.replace('\t', '    ')
