def undo_fix_17_811(code):
def fix_issue_17_811(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
