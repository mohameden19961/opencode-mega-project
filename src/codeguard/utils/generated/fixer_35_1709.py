def undo_fix_35_1709(code):
def fix_issue_35_1709(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
