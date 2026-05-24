def undo_fix_5_218(code):
def fix_issue_5_218(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
