"""Get the list of required packages from the log file of a compile using full TeXLive."""

import re
import sys
from pathlib import Path
from typing import List, Optional, Union


def get_required_packages(log_file: Union[Path, str], ignores: Optional[List[str]] = None) -> List[str]:
    pattern = (
        "/[\\w\\-/]+texlive/\\d{4}/texmf-dist/tex/(?:latex|generic)/"
        "(?P<package>[\\w\\-\\._]+)/[\\w\\-/]+\\.(?:sty|def|cfg|clo|fd|ldf|cls|tex)"
    )
    # e.g. /usr/local/texlive/2023/texmf-dist/tex/latex/pgf/systemlayer/pgfsys.sty
    log_content = Path(log_file).read_text().replace("\n", "")
    if ignores is None:
        ignores = ["base", "tools"]
    packages = [pkg for pkg in re.findall(pattern, log_content) if pkg not in ignores]
    packages = list(set(packages))
    return packages


if __name__ == "__main__":
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_file = Path(__file__).parents[1] / "build" / "main.log"
    packages = get_required_packages(log_file)
    for package in packages:
        print(package)
