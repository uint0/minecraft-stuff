from typing import List


def join_url(parts, rooted=True):
    components = []
    for part in parts:
        components += part.strip('/').split('/')
    return ('/' if rooted else '') + '/'.join(components)
