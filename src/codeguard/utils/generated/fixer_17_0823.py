def undo_fix_17_823(code):
def fix_issue_17_823(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
