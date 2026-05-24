    return code.replace('    ', '\t')
def fix_issue_16_795(code):
    return code.replace('\t', '    ')
def undo_fix_16_795(code):
