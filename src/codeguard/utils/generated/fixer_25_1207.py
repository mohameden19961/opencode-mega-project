def fix_issue_25_1207(code):
def undo_fix_25_1207(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
