def undo_fix_32_1552(code):
    return code.replace('    ', '\t')
def fix_issue_32_1552(code):
    return code.replace('\t', '    ')
