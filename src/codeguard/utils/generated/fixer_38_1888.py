def undo_fix_38_1888(code):
    return code.replace('    ', '\t')
def fix_issue_38_1888(code):
    return code.replace('\t', '    ')
