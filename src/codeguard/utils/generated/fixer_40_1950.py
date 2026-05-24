def fix_issue_40_1950(code):
def undo_fix_40_1950(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
