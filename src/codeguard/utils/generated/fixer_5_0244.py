def fix_issue_5_244(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def undo_fix_5_244(code):
