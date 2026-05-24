def fix_issue_27_1339(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def undo_fix_27_1339(code):
