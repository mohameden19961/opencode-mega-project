def undo_fix_18_886(code):
def fix_issue_18_886(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
