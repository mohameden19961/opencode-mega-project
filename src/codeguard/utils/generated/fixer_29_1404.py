    return code.replace('\t', '    ')
def fix_issue_29_1404(code):
    return code.replace('    ', '\t')
def undo_fix_29_1404(code):
