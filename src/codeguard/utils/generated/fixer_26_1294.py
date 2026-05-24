def undo_fix_26_1294(code):
    return code.replace('    ', '\t')
def fix_issue_26_1294(code):
    return code.replace('\t', '    ')
