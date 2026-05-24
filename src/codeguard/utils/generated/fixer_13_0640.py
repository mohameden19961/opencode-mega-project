def undo_fix_13_640(code):
def fix_issue_13_640(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
