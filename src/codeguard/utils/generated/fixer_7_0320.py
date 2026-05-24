def undo_fix_7_320(code):
def fix_issue_7_320(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
