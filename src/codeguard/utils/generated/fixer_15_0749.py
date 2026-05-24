def fix_issue_15_749(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
