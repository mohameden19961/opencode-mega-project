def undo_fix_20_963(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def fix_issue_20_963(code):
