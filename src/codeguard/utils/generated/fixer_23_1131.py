def undo_fix_23_1131(code):
def fix_issue_23_1131(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
