def fix_issue_39_1913(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
