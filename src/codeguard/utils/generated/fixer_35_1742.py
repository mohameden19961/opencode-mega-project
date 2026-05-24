def fix_issue_35_1742(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def undo_fix_35_1742(code):
