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
from datetime import datetime
from pathlib import Path

_PROJECT_DIR = Path(__file__).resolve().parent
_PROGRAM_TYPES = ["youth", "general", "key", "dedicated", "y", "g", "k", "d"]


def create_application(program_type: str, program_name: str):
    # check program type
    if program_type not in _PROGRAM_TYPES:
        print(f"Invalid program type. Choose from {_PROGRAM_TYPES}")
        sys.exit(1)

    raw_type = {
        "y": "youth",
        "g": "general",
        "k": "key",
        "d": "dedicated",
    }.get(program_type, program_type)

    # abort for not-yet-updated templates
    if raw_type in ["key", "dedicated"]:
        print(f"Error: The template for '{raw_type}' program has not been updated yet.")
        print("Creation aborted.")
        sys.exit(1)

    full_program_type = f"{raw_type}-program"

    # set up paths
    program_dir = _PROJECT_DIR / full_program_type / program_name
    template_dir = _PROJECT_DIR / full_program_type / "template"

    # check existence of target directory
    if program_dir.exists():
        raise FileExistsError(f"The program directory {str(program_dir.relative_to(_PROJECT_DIR))} already exists")

    if not template_dir.exists():
        raise FileNotFoundError(f"Template directory not found: {template_dir}")

    # copy template
    shutil.copytree(template_dir, program_dir)

    # Get the year aggregation file for prompt (look for 20xx.tex in the sibling directory)
    try:
        total_agg_file = [file for file in program_dir.parent.iterdir() if re.search(r"^\d{4}\.tex$", file.name)][0]
        agg_file_rel = str(total_agg_file.relative_to(_PROJECT_DIR))
    except IndexError:
        agg_file_rel = f"{datetime.now().year}.tex"

    # Output success and operation prompt
    print("-" * 60)
    print(f"Created a new application for {raw_type} '{program_name}'")
    print(f"Location: {str(program_dir.relative_to(_PROJECT_DIR))}")
    print("-" * 60)
    print("Action Required:")
    print(f"Please modify the aggregation file: {agg_file_rel}")
    print("Add your new files to the main list, for example:")
    print(f"  \\input{{{full_program_type}/{program_name}/1-立项依据}}")
    print(f"  \\input{{{full_program_type}/{program_name}/2-研究内容}}")
    print("  ...")
    print("-" * 60)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "help":
        print("Usage: python create.py [program-type] [program-name]")
        print("Types: youth(y), general(g), key(k), dedicated(d)")
        sys.exit(0)
    elif len(sys.argv) != 3:
        print("Usage: python create.py [program-type] [program-name]")
        print("Use 'python create.py help' for more information")
        sys.exit(1)

    program_type = sys.argv[1]
    program_name = sys.argv[2]

    create_application(program_type, program_name)
