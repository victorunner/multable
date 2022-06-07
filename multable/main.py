import pathlib
import shutil
import subprocess
import sys
import tempfile
from importlib import util
from typing import Optional, Union

import pydantic_argparse
from argparse_model import Arguments


def run_cmd(
    args: list[str],
    cwd: Union[str, pathlib.Path],
    cmd_description: str,
    verbose_output: bool = False,
):
    capture_output = not verbose_output
    completed = subprocess.run(
        args, cwd=cwd, capture_output=capture_output, text=True, check=False
    )
    # To prevent error `pythontex: error: unrecognized arguments:`
    # under debugging in VS Code
    # use subprocess.run('pythontex tempalte.tex', shell=True, ...)
    # or
    # add `"subProcess": false` to launch.json

    if completed.returncode != 0:
        sys.exit(cmd_description + ' run failed')


def cli(args: Optional[list[str]] = None) -> None:
    if not args:
        args = sys.argv[1:]

    parser = pydantic_argparse.ArgumentParser(
        model=Arguments,
        prog='multable',
        description='Generates multiplication table in arabic/slavic language',
        version='0.0.1',
        exit_on_error=True,
    )
    args_model = parser.parse_typed_args(args)
    verbose = args_model.verbose
    output_file_path = args_model.output
    if output_file_path is None:
        verbose = False
    args_as_json = args_model.json()

    argparse_model_path = pathlib.Path(__file__).parent / 'argparse_model.py'

    texresource_spec = util.find_spec('texresource')
    if not texresource_spec or not texresource_spec.origin:
        sys.exit('texresource package not found.')

    texresource_path = pathlib.Path(texresource_spec.origin).parent
    template_tex_path = texresource_path / 'template.tex'
    import_input_tex_path = texresource_path / 'import_input.tex'

    with tempfile.TemporaryDirectory() as tmpdir_path_str:
        tmpdir_path = pathlib.Path(tmpdir_path_str)

        (tmpdir_path / 'input.json').write_text(args_as_json)

        shutil.copy(template_tex_path, tmpdir_path)
        shutil.copy(import_input_tex_path, tmpdir_path)
        shutil.copy(argparse_model_path, tmpdir_path)

        run_cmd(
            [
                'lualatex',
                '--interaction=nonstopmode',
                '--synctex=1',
                '--shell-escape',
                '--file-line-error',
                'template.tex',
            ],
            cwd=tmpdir_path_str,
            cmd_description='lualatex',
            verbose_output=verbose,
        )

        run_cmd(
            ['pythontex', 'template.tex'],
            cwd=tmpdir_path_str,
            cmd_description='pythontex',
            verbose_output=verbose,
        )

        run_cmd(
            [
                'lualatex',
                '--interaction=nonstopmode',
                '--synctex=1',
                '--shell-escape',
                '--file-line-error',
                'template.tex',
            ],
            cwd=tmpdir_path_str,
            cmd_description='lualatex (final)',
            verbose_output=verbose,
        )

        result_pdf_path = tmpdir_path / 'template.pdf'

        if output_file_path is None:
            with open(result_pdf_path, 'rb') as f:
                # sys.stdout.buffer.write(f.read())  # noqa: E800
                shutil.copyfileobj(f, sys.stdout.buffer)   # coping in chunks
        else:
            shutil.copy2(result_pdf_path, output_file_path)


if __name__ == '__main__':
    cli()
