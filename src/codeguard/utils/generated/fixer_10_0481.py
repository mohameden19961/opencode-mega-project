def undo_fix_10_481(code):
    return code.replace('\t', '    ')
def fix_issue_10_481(code):
    return code.replace('    ', '\t')
