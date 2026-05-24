def undo_fix_27_1308(code):
def fix_issue_27_1308(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
