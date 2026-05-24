def fix_issue_16_759(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
def undo_fix_16_759(code):
