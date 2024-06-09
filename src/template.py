import re

from config import get_attune_file_path, get_repo_file_path

def template_apply(s):
    replacements = {
        "paths.config": get_attune_file_path().replace('\\', '/'),
        "paths.repo": get_repo_file_path().replace('\\', '/')
    } 

    def replacer(match):
        token = match.group(1)
        return replacements.get(token, match.group(0))
    
    pattern = re.compile(r'{{(.*?)}}')
    result = pattern.sub(replacer, s)
    return result