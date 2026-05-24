def fix_issue_22_1085(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
