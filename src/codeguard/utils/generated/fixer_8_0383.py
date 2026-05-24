def undo_fix_8_383(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
def fix_issue_8_383(code):
