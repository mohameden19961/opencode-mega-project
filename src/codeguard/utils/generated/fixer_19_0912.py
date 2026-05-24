    return code.replace('    ', '\t')
def fix_issue_19_912(code):
    return code.replace('\t', '    ')
def undo_fix_19_912(code):
