def undo_fix_27_1323(code):
def fix_issue_27_1323(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
