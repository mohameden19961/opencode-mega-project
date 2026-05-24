def fix_issue_18_898(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def undo_fix_18_898(code):
