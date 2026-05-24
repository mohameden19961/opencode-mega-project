def undo_fix_32_1591(code):
    return code.replace('\t', '    ')
def fix_issue_32_1591(code):
    return code.replace('    ', '\t')
