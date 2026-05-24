def undo_fix_10_450(code):
def fix_issue_10_450(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
