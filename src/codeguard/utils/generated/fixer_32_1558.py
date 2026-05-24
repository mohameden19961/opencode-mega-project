def undo_fix_32_1558(code):
def fix_issue_32_1558(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
