def undo_fix_28_1364(code):
    return code.replace('    ', '\t')
def fix_issue_28_1364(code):
    return code.replace('\t', '    ')
