import os
from abc import ABC, abstractmethod
from typing import List, Dict
import click as clk


class Stat(ABC):
    """ Base class for a stat based on files processing """

    @abstractmethod
    def consume(self, root: str, file: str, ext: str) -> None:
        """ Callback method for processing single file

        :param root: Base folder of a file
        :param file: File path
        :param ext: File extension
        """
        pass


class FilesCount(Stat):
    """ Calculates a number of files """
    def __init__(self):
        self._count: int = 0

    def consume(self, root: str, file: str, ext: str) -> None:
        self._count += 1

    def count(self) -> int:
        return self._count


class Extensions(Stat):
    """ Collects extensions """
    def __init__(self):
        self._exts: set[str] = set()

    def consume(self, root: str, file: str, ext: str) -> None:
        self._exts.add(ext)

    def extensions(self) -> set:
        return self._exts


class Loc(Stat):
    """ Collects lines of code """
    def __init__(self):
        self._count: int = 0
        self._max: int = 0

    def consume(self, root: str, file: str, ext: str) -> None:
        with open(file, 'r', encoding='utf8') as f:
            loc_in_file = sum(1 for _ in f)
            self._count += loc_in_file
            self._max = max(self._max, loc_in_file)

    def total(self) -> int:
        return self._count

    def max(self) -> int:
        return self._max


class Repo:
    """ Repo represented by a folder """
    def __init__(self,
                 repo: str,
                 incl: List[str] = None,
                 excl: List[str] = None,
                 stats: Dict[str, Stat] = None,
                 incl_stats: Dict[str, Stat] = None,
                 excl_stats: Dict[str, Stat] = None):
        """

        :param repo: Repo path
        :param incl: Extensions to be included
        :param excl: Extensions to be excluded
        :param stats: Stats calculated for all files
        :param incl_stats: Stats calculated for included files only
        :param excl_stats: Stats calculated for excluded files only
        """
        self._repo = repo
        self._incl = incl
        self._excl = excl
        self._stats = stats
        self._incl_stats = incl_stats
        self._excl_stats = excl_stats

    def iterate(self):
        """ Iterates over a folder applying incl/excl filter
            and calling corresponding stats calculation.
        """
        for root, _, files in os.walk(self._repo):
            for file in files:
                _, ext = os.path.splitext(file)
                [stat.consume(root, file, ext) for stat in self._stats.values()]
                if (self._incl and ext not in self._incl
                        or self._excl and ext in self._excl):
                    [stat.consume(root, file, ext) for stat in self._excl_stats.values()]
                else:
                    [stat.consume(root, file, ext) for stat in self._incl_stats.values()]


@clk.command()
@clk.option('--incl', '-i', 'ext_incl', multiple=True, default=[],
            help="Extensions to include")
@clk.option('--excl', '-e', 'ext_excl', multiple=True, default=[],
            help="Extensions to exclude")
@clk.argument('repo_path', type=clk.Path(exists=True))
def print_stat(repo_path: str, ext_incl: List, ext_excl: List):
    """ Prints stats for given repo (folder).
    """

    for_all = {
        'Files': FilesCount()
    }
    included_only = {
        'Matched files': FilesCount(),
        'LoC': Loc(),
        'Matched extensions': Extensions()
    }
    excluded_only = {
        'Excluded files': FilesCount(),
        'Excluded extensions': Extensions()
    }

    Repo(
        repo_path,
        stats=for_all,
        incl_stats=included_only,
        excl_stats=excluded_only,
        excl=ext_excl,
        incl=ext_incl
    ).iterate()

    files_total = for_all['Files'].count()
    loc_total = included_only['LoC'].total()
    loc_max = included_only['LoC'].max()

    print(f'Repo: {os.path.abspath(repo_path)}')
    print(f'Inclusions: {ext_incl}')
    print(f'Exclusions: {ext_excl}')
    print(f'Files total: {files_total}')
    print(f'Extensions excluded: {excluded_only['Excluded extensions']
          .extensions()}')
    print(f'Files matched: {included_only['Matched files'].count()}')
    print(f'Files excluded: {excluded_only['Excluded files'].count()}')
    print(f'LoC total: {loc_total}')
    print(f'LoC avg: {loc_total / files_total}')
    print(f'LoC max: {loc_max}')
    print(f'Extensions: {included_only['Matched extensions'].extensions()}')


if __name__ == '__main__':
    print_stat()

