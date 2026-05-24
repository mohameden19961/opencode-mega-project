def undo_fix_36_1755(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
def fix_issue_36_1755(code):
