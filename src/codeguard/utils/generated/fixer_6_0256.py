def fix_issue_6_256(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
