def fix_issue_15_744(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
