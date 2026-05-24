def undo_fix_19_941(code):
    return code.replace('    ', '\t')
def fix_issue_19_941(code):
    return code.replace('\t', '    ')
