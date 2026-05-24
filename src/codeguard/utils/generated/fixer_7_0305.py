def undo_fix_7_305(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
def fix_issue_7_305(code):
