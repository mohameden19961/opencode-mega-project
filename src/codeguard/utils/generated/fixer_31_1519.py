def fix_issue_31_1519(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
