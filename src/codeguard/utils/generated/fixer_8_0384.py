def undo_fix_8_384(code):
def fix_issue_8_384(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
