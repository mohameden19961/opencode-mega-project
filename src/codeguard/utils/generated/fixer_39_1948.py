def fix_issue_39_1948(code):
    return code.replace('\t', '    ')
def undo_fix_39_1948(code):
    return code.replace('    ', '\t')
