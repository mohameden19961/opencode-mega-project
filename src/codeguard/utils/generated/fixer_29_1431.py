def fix_issue_29_1431(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
