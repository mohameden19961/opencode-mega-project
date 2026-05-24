def undo_fix_38_1882(code):
def fix_issue_38_1882(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
