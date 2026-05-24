    return code.replace('\t', '    ')
def fix_issue_7_343(code):
def undo_fix_7_343(code):
    return code.replace('    ', '\t')
