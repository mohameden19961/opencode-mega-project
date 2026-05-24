def undo_fix_13_643(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def fix_issue_13_643(code):
