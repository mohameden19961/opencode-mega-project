def fix_issue_11_513(code):
def undo_fix_11_513(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
