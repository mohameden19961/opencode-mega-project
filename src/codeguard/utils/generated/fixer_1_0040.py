def undo_fix_1_40(code):
    return code.replace('    ', '\t')
def fix_issue_1_40(code):
    return code.replace('\t', '    ')
