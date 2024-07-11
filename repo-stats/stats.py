import os
from typing import List


def loc(file: str) -> int:
    """ Calculates lines in a file """
    with open(file, 'r', encoding='utf8') as f:
        return sum(1 for _ in f)


def print_stat(repo_path: str, ext_incl: List, ext_excl: List):
    """ Prints stats for given repo

    :param repo_path: Path to a repo
    :param ext_incl: Extensions to include (priority). Ex.: ['.png', '.css']
    :param ext_excl: Extensions to exclude. Ex.: ['.java', '.xml']
    """
    files_total: int = 0
    loc_total: int = 0
    extensions = {}

    for root, _, files in os.walk(repo_path):
        for file in files:
            files_total += 1
            _, extension = os.path.splitext(file)
            if (ext_incl and extension not in ext_incl
                    or not ext_excl and extension in ext_excl):
                continue

            if extension not in extensions:
                extensions[extension] = (1, 0)

            ext_files = extensions[extension][0] + 1
            ext_loc = extensions[extension][1]

            try:
                file_loc = loc(root + '/' + file)
                loc_total += file_loc
                ext_loc += file_loc
            except Exception as ex:
                print(f'Unable to read file {root + "/" + file}: {ex}')

            extensions[extension] = (ext_files, ext_loc)

    print(f'Repo: {os.path.abspath(repo_path)}')
    print(f'Inclusions: {ext_incl}')
    print(f'Exclusions: {ext_excl}')
    print(f'Files total: {files_total}')
    print(f'LoC total: {loc_total}')
    print(f'Extensions: {extensions}')


if __name__ == '__main__':
    print_stat('./', ['.py', '.md'], [])

