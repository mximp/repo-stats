import os
from typing import List
import click as clk


def loc(file: str) -> int:
    """ Calculates lines in a file """
    with open(file, 'r', encoding='utf8') as f:
        return sum(1 for _ in f)


@clk.command()
@clk.option('--incl', '-i', 'ext_incl', multiple=True, default=[])
@clk.option('--excl', '-e', 'ext_excl', multiple=True, default=[])
@clk.argument('repo_path', type=clk.Path(exists=True))
def print_stat(repo_path: str, ext_incl: List, ext_excl: List):
    """ Prints stats for given repo

    :param repo_path: Path to a repo
    :param ext_incl: Extensions to include (priority). Ex.: ['.png', '.css']
    :param ext_excl: Extensions to exclude. Ex.: ['.java', '.xml']
    """
    files_total: int = 0
    files_matched: int = 0
    loc_total: int = 0
    loc_max: int = 0
    extensions = {}
    extensions_excluded = set()

    for root, _, files in os.walk(repo_path):
        for file in files:
            files_total += 1
            _, extension = os.path.splitext(file)
            if (ext_incl and extension not in ext_incl
                    or ext_excl and extension in ext_excl):
                extensions_excluded.add(extension)
                continue

            files_matched += 1

            if extension not in extensions:
                # files / LoC / LoC avg / LoC max
                extensions[extension] = (0, 0, 0, 0)

            ext_files = extensions[extension][0] + 1
            ext_loc = extensions[extension][1]
            ext_loc_max = extensions[extension][3]

            try:
                file_loc = loc(root + '/' + file)
                ext_loc_max = max(ext_loc_max, file_loc)
                loc_max = max(loc_max, file_loc)
                loc_total += file_loc
                ext_loc += file_loc
            except Exception as ex:
                print(f'Unable to read file {root + "/" + file}: {ex} ')

            extensions[extension] \
                = (ext_files, ext_loc, ext_loc / ext_files, ext_loc_max)

    print(f'Repo: {os.path.abspath(repo_path)}')
    print(f'Inclusions: {ext_incl}')
    print(f'Exclusions: {ext_excl}')
    print(f'Files total: {files_total}')
    print(f'Extensions excluded: {extensions_excluded}')
    print(f'Files matched: {files_matched}')
    print(f'LoC total: {loc_total}')
    print(f'LoC avg: {loc_total / files_total}')
    print(f'LoC max: {loc_max}')
    print(f'Extensions: {extensions}')


if __name__ == '__main__':
    print_stat()

