import os
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
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
    """ Calculates a number of files per extension"""
    def __init__(self):
        self._ext: Dict[str, int] = {}

    def consume(self, root: str, file: str, ext: str) -> None:
        if ext not in self._ext:
            self._ext[ext] = 0
        self._ext[ext] += 1

    def total(self) -> int:
        return sum(count for count in self._ext.values())

    def ext_count(self, ext: str) -> int:
        return self._ext[ext]


class Extensions(Stat):
    """ Collects extensions """
    def __init__(self):
        self._exts: set[str] = set()

    def consume(self, root: str, file: str, ext: str) -> None:
        self._exts.add(ext)

    def all(self) -> set:
        return self._exts


class Loc(Stat):
    """ Collects lines of code (LoC) per extension.
    Calculates total and maximum per extension.
    """
    def __init__(self):
        self._ext: Dict[str, Tuple[int, int]] = {}

    def consume(self, root: str, file: str, ext: str) -> None:
        with open(root + '/' + file, 'r', encoding='utf8') as f:
            in_file = sum(1 for _ in f)
            if ext not in self._ext:
                self._ext[ext] = (0, 0)
            ext_total, ext_max = self._ext[ext]
            self._ext[ext] = (
                ext_total + in_file,
                max(ext_max, in_file)
            )

    def total(self) -> int:
        return sum(count[0] for count in self._ext.values())

    def loc(self, ext: str) -> int:
        return self._ext[ext][0]

    def max(self):
        return sum(count[1] for count in self._ext.values())

    def ext_max(self, ext: str) -> int:
        return self._ext[ext][1]


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
                    [stat.consume(root, file, ext)
                     for stat in self._excl_stats.values()]
                else:
                    [stat.consume(root, file, ext)
                     for stat in self._incl_stats.values()]


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

    files_total = for_all['Files'].total()
    loc_total = included_only['LoC'].total()
    loc_max = included_only['LoC'].max()
    ext_loc_stats = {
        ext: (
            included_only['LoC'].loc(ext),
            included_only['LoC'].ext_max(ext),
            included_only['LoC'].loc(ext) / included_only['Matched files'].ext_count(ext)
        )
        for ext in included_only['Matched extensions'].all()
    }

    print(f'Repo: {os.path.abspath(repo_path)}')
    print(f'Inclusions: {ext_incl}')
    print(f'Exclusions: {ext_excl}')
    print(f'Files total: {files_total}')
    print(f'Extensions excluded: {excluded_only['Excluded extensions'].all()}')
    print(f'Files matched: {included_only['Matched files'].total()}')
    print(f'Files excluded: {excluded_only['Excluded files'].total()}')
    print(f'LoC total: {loc_total}')
    print(f'LoC avg: {loc_total / files_total}')
    print(f'LoC max: {loc_max}')
    print(f'Extensions (files/max/avg): {ext_loc_stats}')


if __name__ == '__main__':
    print_stat()

