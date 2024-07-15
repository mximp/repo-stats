# Repository statistics

Collects various repository statistics such as files count by type or lines of code.

## Installation

## Usage

As Python module:
```shell
python -m stats /path/to/repo/ ".py .java"  
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

