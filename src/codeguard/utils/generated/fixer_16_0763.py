def undo_fix_16_763(code):
def fix_issue_16_763(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
