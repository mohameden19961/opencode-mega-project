def fix_issue_39_1918(code):
def undo_fix_39_1918(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
