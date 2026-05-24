def fix_issue_23_1115(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def undo_fix_23_1115(code):
