"""
Create a new application for NSFC program.

Usage:

```bash
python create.py [program-type] [program-name]
```

where `program-type` is one of the following:

- `youth`: NSFC Youth Program (青年基金), alias `y`
- `general`: NSFC General Program (面上项目), alias `g`
- `key`: NSFC Key Program (重点项目), alias `k`
- `dedicated`: NSFC Dedicated Program (专项项目), alias `d`

"""

import re
import shutil
import sys
import warnings
from datetime import datetime
from pathlib import Path

_PROJECT_DIR = Path(__file__).resolve().parent
_PROGRAM_TYPES = ["youth", "general", "key", "dedicated", "y", "g", "k", "d"]


def create_application(program_type: str, program_name: str):
    if program_type not in _PROGRAM_TYPES:
        raise ValueError(f"Invalid program type. Choose from {_PROGRAM_TYPES}")
    program_type = {
        "y": "youth",
        "g": "general",
        "k": "key",
        "d": "dedicated",
    }.get(program_type, program_type)
    program_type = f"{program_type}-program"

    current_year = datetime.now().year

    # Create a new directory
    program_dir = _PROJECT_DIR / program_type / program_name
    if program_dir.exists():
        raise FileExistsError(f"The program directory {str(program_dir.relative_to(_PROJECT_DIR))} already exists")

    if not (program_dir.parent / f"{current_year}.tex").exists():
        warnings.warn(
            f"The template for the program type '{program_type.split('-')[0]}' "
            "might not be up-to-date. Please check the template files at the official website."
        )

    template_dir = _PROJECT_DIR / program_type / "template"
    # copy everything from the template directory to the new directory
    shutil.copytree(template_dir, program_dir)

    # modify the file "1-立项依据与研究内容/aggregate.tex" in the new directory
    # by replacing "\input{program_type/template/" with "\input{program_type/program_name/"
    part1_agg_file = program_dir / "1-立项依据与研究内容" / "aggregate.tex"
    part1_agg_file_content = part1_agg_file.read_text()
    part1_agg_file_content = part1_agg_file_content.replace(
        f"\\input{{{program_type}/template/", f"\\input{{{program_type}/{program_name}/"
    )
    part1_agg_file.write_text(part1_agg_file_content)

    # find total_agg_file in program_dir, which is of the form "year.tex"
    total_agg_file = [file for file in program_dir.parent.iterdir() if re.search("^\\d{4}\\.tex$", file.name) is not None][0]

    print(
        f"Created a new application for {program_type.replace('-', ' ')} '{program_name}' "
        f"in the folder {str(program_dir.relative_to(_PROJECT_DIR))}"
    )
    print(
        "Please make corresponding modifications in the "
        f"aggregation file {str(total_agg_file.relative_to(_PROJECT_DIR))}, "
        "and include it in the main file main.tex."
    )


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "help":
        print(__doc__)
        sys.exit(0)
    elif len(sys.argv) != 3:
        print("Usage: python create.py [program-type] [program-name]")
        print("Use 'python create.py help' for more information")
        sys.exit(1)

    program_type = sys.argv[1]
    program_name = sys.argv[2]

    if program_type not in ["youth", "general", "key", "dedicated", "y", "g", "k", "d"]:
        print(f"Invalid program type. Choose from {_PROGRAM_TYPES}")
        sys.exit(1)

    create_application(program_type, program_name)
