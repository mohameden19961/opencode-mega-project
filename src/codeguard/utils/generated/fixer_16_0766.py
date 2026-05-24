def fix_issue_16_766(code):
    return code.replace('\t', '    ')
def undo_fix_16_766(code):
    return code.replace('    ', '\t')
