def fix_issue_27_1317(code):
def undo_fix_27_1317(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
