def undo_fix_40_1985(code):
def fix_issue_40_1985(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
