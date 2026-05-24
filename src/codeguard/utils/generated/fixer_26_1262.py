def undo_fix_26_1262(code):
def fix_issue_26_1262(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
