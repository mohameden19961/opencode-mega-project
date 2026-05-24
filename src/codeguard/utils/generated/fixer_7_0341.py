    return code.replace('    ', '\t')
def fix_issue_7_341(code):
    return code.replace('\t', '    ')
def undo_fix_7_341(code):
