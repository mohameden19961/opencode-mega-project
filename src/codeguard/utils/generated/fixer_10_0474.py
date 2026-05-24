def fix_issue_10_474(code):
    return code.replace('\t', '    ')
def undo_fix_10_474(code):
    return code.replace('    ', '\t')
