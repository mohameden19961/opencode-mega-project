def fix_issue_1_18(code):
    return code.replace('\t', '    ')
def undo_fix_1_18(code):
    return code.replace('    ', '\t')
