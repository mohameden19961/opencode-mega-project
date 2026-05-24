def fix_issue_30_1453(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
