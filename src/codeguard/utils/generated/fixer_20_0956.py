def fix_issue_20_956(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
def undo_fix_20_956(code):
