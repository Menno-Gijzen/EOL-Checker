# EOL-Checker

A CLI tool that fetches software products reaching End-of-Life (EOL) in a given year from [endoflife.date](https://endoflife.date) and exports the results to a CSV file.

## Features

- Queries the [endoflife.date API](https://endoflife.date/docs/api) for all tracked software products
- Filters products by a user-specified EOL year
- Exports matching products (name, EOL date, cycle) to a CSV file
- Configurable output directory via `--output` flag

## Requirements

- Python 3.6+
- [requests](https://pypi.org/project/requests/)

## Installation

```bash
git clone https://github.com/yourusername/EOL-Checker.git
cd EOL-Checker
pip install requests
```

## Usage

```bash
python eol.py
```

You will be prompted to enter a 4-digit year (e.g. `2026`). The tool then queries every product on endoflife.date and writes matches to `~/eol/eol_<year>.csv`.

### Custom output directory

```bash
python eol.py --output /path/to/folder
```

### Example output

```
Found 142 products with an EOL in 2026.
Data exported to /home/user/eol/eol_2026.csv
```

The generated CSV contains three columns:

| Product | EOLDate | Cycle |
|---------|---------|-------|
| nodejs  | 2026-04-30 | 20 |
| ubuntu  | 2026-04-01 | 21.10 |

## How it works

1. Fetches the full product list from `https://endoflife.date/api/all.json`
2. For each product, retrieves its version/cycle details
3. Checks if any cycle has an EOL date matching the target year
4. Collects the first matching cycle per product and writes the results to CSV

## License

This project is licensed under the [MIT License](LICENSE).

## Author

[@Menno_Gijzen_](https://twitter.com/Menno_Gijzen_)
