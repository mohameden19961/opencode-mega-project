def fix_issue_3_109(code):
def undo_fix_3_109(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
