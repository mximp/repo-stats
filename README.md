# Repository statistics

Collects various repository statistics such as files count by type or lines of code.

## Installation

Just clone this repo:
```shell
git clone https://github.com/mximp/repo-stats.git
```

## Usage

As Python module:
```shell
python -m stats -i ".java" -i ".py" /path/to/repo/  
```

Output example:
```shell
Repo: /path/to/repo
Inclusions: ['.py', '.java']
Exclusions: []
Files total: 322
Extensions excluded: {'.md', '', '.idx', '.zip'}
Files matched: 286
LoC total: 8064
LoC avg: 25
LoC max: 183
Extensions: {'.py': (280, 8000, 28, 183), '.java': (6, 64, 10, 100)}
```

## Collected stats

