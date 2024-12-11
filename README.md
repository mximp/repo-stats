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
#runs under `repo-stats/repo-stats` folder
python -m stats -i ".java" -i ".py" /path/to/repo/  
```

Output example:
```shell
Repo: /path/to/repo
Inclusions spec: ('.java',)
Exclusions spec: ()
Files total: 63
Extensions excluded: {'', '.properties', '.md', '.xml', '.class', '.pack', '.jar', '.yml', '.sample', '.lst', '.iml', '.idx'}
Files matched: 2
Files excluded: 61
LoC total: 89
LoC avg: 44.5
LoC max: 82
Classes: 13
Extensions (LoC/max/avg): {'.java': (89, 82, 44.5)}
```

## Stats

The following statistics is being collected:

- `Files total`: total number of files found in the repo
- `Files matched`: number of files which matched provided criteria, i.e. inclusion/exclusion spec
- `LoC total`: total lines within matched files
- `LoC avg`: average number of lines per file across all matched files
- `LoC max`: maximum number of lines in a file acrosss all matched files
- `Classes`: number of classes found in matched files (.java and .py supported)
- `Extensions`: total, max, and average LoC per file extension.



