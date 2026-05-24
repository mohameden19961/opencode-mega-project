def fix_issue_25_1231(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
