def undo_fix_11_503(code):
def fix_issue_11_503(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
