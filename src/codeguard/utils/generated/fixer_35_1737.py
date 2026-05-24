def fix_issue_35_1737(code):
    return code.replace('    ', '\t')
def undo_fix_35_1737(code):
    return code.replace('\t', '    ')
