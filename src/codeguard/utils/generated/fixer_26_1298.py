def fix_issue_26_1298(code):
    return code.replace('    ', '\t')
def undo_fix_26_1298(code):
    return code.replace('\t', '    ')
