def fix_issue_38_1884(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
