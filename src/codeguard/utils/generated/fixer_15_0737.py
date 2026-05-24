def undo_fix_15_737(code):
    return code.replace('    ', '\t')
def fix_issue_15_737(code):
    return code.replace('\t', '    ')
