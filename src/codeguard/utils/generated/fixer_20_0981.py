def fix_issue_20_981(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def undo_fix_20_981(code):
