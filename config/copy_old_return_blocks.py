#!/usr/bin/env python
import os
import yaml


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
OLD_MODULE_PATH = f"{SCRIPT_DIR}/../../temp/vmware.vmware_rest/plugins/modules"
NEW_MODULE_PATH = f"{SCRIPT_DIR}/output/plugins/modules"
GALAXY_PATH = f"{SCRIPT_DIR}/../galaxy.yml"


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


def read_version_added(old_module_file_path):
    with open(old_module_file_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("version_added:"):
            return line

    return None


def format_new_content(module_file_path, example_and_return_blocks, version_added):
    with open(module_file_path, "r") as f:
        lines = f.readlines()

    with open(GALAXY_PATH, "r") as f:
        _galaxy_contents = yaml.safe_load(f)
        default_version = _galaxy_contents["version"]

    new_content = []
    added_content = False
    open_block = False
    for line in lines:
        if example_and_return_blocks and (
            line.startswith('EXAMPLES = r"""') or line.startswith('RETURN = r"""')
        ):
            open_block = True
            if not added_content:
                new_content += example_and_return_blocks
                added_content = True
            continue

        if open_block and line.startswith('"""'):
            open_block = False
            continue

        if line.startswith("version_added"):
            if version_added:
                new_content += [version_added]
            else:
                new_content += [f"version_added: {default_version}\n"]
            continue

        new_content += [line]

    return new_content


if __name__ == "__main__":
    for module in os.listdir(NEW_MODULE_PATH):
        old_module = os.path.join(OLD_MODULE_PATH, module)
        new_module = os.path.join(NEW_MODULE_PATH, module)
        blocks = []
        version_added = None
        if os.path.isfile(old_module):
            blocks = read_examples_and_return_blocks(old_module)
            version_added = read_version_added(old_module)

        new_content = format_new_content(new_module, blocks, version_added)
        with open(new_module, "w") as f:
            for line in new_content:
                f.write(f"{line}")
