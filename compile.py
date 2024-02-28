import collections
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple, Union

project_dir = Path(__file__).resolve().parent
build_dir = project_dir / "build"
if not build_dir.exists():
    build_dir.mkdir(parents=True, exist_ok=True)
main_tex_file = project_dir / "main.tex"


def execute_cmd(cmd: Union[str, List[str]], raise_error: bool = True) -> Tuple[int, List[str]]:
    """Execute shell command using `Popen`.

    Parameters
    ----------
    cmd : str or list of str
        Shell command to be executed,
        or a list of .sh files to be executed.
    raise_error : bool, default True
        If True, error will be raised when occured.

    Returns
    -------
    exitcode : int
        Exit code returned by `Popen`.
    output_msg : list of str
        Outputs from `stdout` of `Popen`.

    """
    shell_arg, executable_arg = True, None
    s = subprocess.Popen(
        cmd,
        shell=shell_arg,
        executable=executable_arg,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        close_fds=(not (platform.system().lower() == "windows")),
    )
    debug_stdout = collections.deque(maxlen=1000)
    # print("\n" + "*" * 10 + "  execute_cmd starts  " + "*" * 10 + "\n")
    while 1:
        line = s.stdout.readline().decode("utf-8", errors="replace")
        if line.rstrip():
            debug_stdout.append(line)
            print(line)
        exitcode = s.poll()
        if exitcode is not None:
            for line in s.stdout:
                debug_stdout.append(line.decode("utf-8", errors="replace"))
            if exitcode is not None and exitcode != 0:
                error_msg = " ".join(cmd) if not isinstance(cmd, str) else cmd
                error_msg += "\n"
                error_msg += "".join(debug_stdout)
                s.communicate()
                s.stdout.close()
                print("\n" + "*" * 10 + "  execute_cmd failed  " + "*" * 10 + "\n")
                if raise_error:
                    raise subprocess.CalledProcessError(exitcode, error_msg)
                else:
                    output_msg = list(debug_stdout)
                    return exitcode, output_msg
            else:
                break
    s.communicate()
    s.stdout.close()
    output_msg = list(debug_stdout)

    # print("\n" + "*" * 10 + "  execute_cmd succeeded  " + "*" * 10 + "\n")

    exitcode = 0

    return exitcode, output_msg


def main():
    if shutil.which("latexmk") is None:
        raise RuntimeError("latexmk is not installed.")

    if len(sys.argv) not in [1, 2]:
        raise RuntimeError("Usage: python compile.py [tex_entry_file]")
    if len(sys.argv) == 1:
        tex_entry_file = main_tex_file
        handout = True
    else:
        tex_entry_file = Path(sys.argv[1]).expanduser().resolve()
        handout = False

    # specifying outdir for latexmk may result in errors: https://tex.stackexchange.com/q/323820
    cmd = (
        f"""latexmk -xelatex --enable-pipes --shell-escape -f -outdir="{str(project_dir)}" """
        f"""-jobname="{tex_entry_file.stem}" "{str(tex_entry_file)}" """
    )
    try:
        exitcode, _ = execute_cmd(cmd)
    except KeyboardInterrupt:
        # clean up
        cmd = f"""latexmk -C -outdir="{str(project_dir)}" "{str(tex_entry_file)}" """
        execute_cmd(cmd, raise_error=False)
        print("Compilation cancelled.")
        exitcode = 1
    if exitcode != 0:
        sys.exit(exitcode)
    generated_pdf_file = project_dir / f"{main_tex_file.stem}.pdf"
    suffix = time.strftime("%Y%m%d-%H%M%S")
    if main_tex_file.stem == "main" and handout:
        backup_pdf_file = build_dir / f"NSFC申请书示例-{suffix}.pdf"
    else:
        backup_pdf_file = build_dir / f"{main_tex_file.stem}.pdf"
    shutil.copy(generated_pdf_file, backup_pdf_file)
    # also copy the log file
    shutil.copy(generated_pdf_file.with_suffix(".log"), backup_pdf_file.with_suffix(".log"))

    # clean up
    cmd = f"""latexmk -C -outdir="{str(project_dir)}" "{str(tex_entry_file)}" """
    exitcode, _ = execute_cmd(cmd)
    if exitcode != 0:
        sys.exit(exitcode)
    # in case bbl file is not cleaned up
    bbl_file = project_dir / f"{main_tex_file.stem}.bbl"
    if bbl_file.exists():
        bbl_file.unlink()
    # clear files of the pattern xelatex*.fls
    for fls_file in project_dir.glob("xelatex*.fls"):
        fls_file.unlink()


if __name__ == "__main__":
    main()
