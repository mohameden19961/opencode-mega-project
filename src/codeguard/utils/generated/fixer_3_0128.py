def undo_fix_3_128(code):
    return code.replace('    ', '\t')
def fix_issue_3_128(code):
    return code.replace('\t', '    ')
