def fix_issue_12_565(code):
    return code.replace('\t', '    ')
def undo_fix_12_565(code):
    return code.replace('    ', '\t')
