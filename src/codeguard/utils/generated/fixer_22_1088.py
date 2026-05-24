def fix_issue_22_1088(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def undo_fix_22_1088(code):
