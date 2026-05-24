def fix_issue_38_1862(code):
    return code.replace('    ', '\t')
def undo_fix_38_1862(code):
    return code.replace('\t', '    ')
