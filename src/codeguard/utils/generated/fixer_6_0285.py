def undo_fix_6_285(code):
    return code.replace('\t', '    ')
def fix_issue_6_285(code):
    return code.replace('    ', '\t')
