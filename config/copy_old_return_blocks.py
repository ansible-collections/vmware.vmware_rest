#!/usr/bin/env python
import os


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
OLD_MODULE_PATH = f"{SCRIPT_DIR}/../plugins/modules"
NEW_MODULE_PATH = f"{SCRIPT_DIR}/output/plugins/modules"


def read_examples_and_return_blocks(module_file_path):
    with open(module_file_path, "r") as f:
        lines = f.readlines()

    copy_line = False
    content = []
    for line in lines:
        if line.startswith('EXAMPLES = r"""') or line.startswith('RETURN = r"""'):
            copy_line = True

        if copy_line:
            content += [line]

        if line.startswith('"""'):
            copy_line = False

    return content


def inject_examples_and_return_blocks(module_file_path, inject_lines):
    with open(module_file_path, "r") as f:
        lines = f.readlines()

    new_content = []
    added_content = False
    open_block = False
    for line in lines:
        if line.startswith('EXAMPLES = r"""') or line.startswith('RETURN = r"""'):
            open_block = True
            if not added_content:
                new_content += inject_lines
                added_content = True
            continue

        if open_block and line.startswith('"""'):
            open_block = False
            continue

        new_content += [line]

    return new_content


if __name__ == "__main__":
    for module in os.listdir(OLD_MODULE_PATH):
        old_module = os.path.join(OLD_MODULE_PATH, module)
        new_module = old_module.replace(OLD_MODULE_PATH, NEW_MODULE_PATH)
        if os.path.isfile(old_module):
            blocks = read_examples_and_return_blocks(old_module)
            new_content = inject_examples_and_return_blocks(new_module, blocks)

            with open(new_module, "w") as f:
                for line in new_content:
                    f.write(f"{line}")
