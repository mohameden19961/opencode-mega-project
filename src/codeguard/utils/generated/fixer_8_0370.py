def undo_fix_8_370(code):
def fix_issue_8_370(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
