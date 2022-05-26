# -*- coding: utf-8 -*-

import os
import re

from cn_sort.process_cn_word import *


def output_markdown(dir: str, base_dir: str, output_file: str, iter_depth=0):

    """
    Main iterator for get information from every file/folder

    i: directory, base directory(to calulate relative path), output file name, iter depth
    p: Judge is directory or is file, then process .md/.markdown files
    o: write .md information (with identation) to output_file
    """

    ignores = ["_book", "docs", "images", "node_modules", "dict", ".git"]

    for filename in sort_dir_file(os.listdir(dir), base_dir):

        # add list and sort
        if filename in ignores:
            print("continue ", filename)  # output log
            continue
        print("Processing ", filename)  # output log

        file_or_path = os.path.join(dir, filename)

        if os.path.isdir(file_or_path):  # is dir
            if mdfile_in_dir(file_or_path):

                createRead0(file_or_path, "0-README.md")

                # if there is .md file in the folder, output the folder name Excluding the serial number like 1-.
                output_file.write(
                    "  " * iter_depth
                    + "* [{}]({}/{})\n".format(
                        re.sub(r"^[0-9A-Z]+-", "", filename), filename, "0-README.md"
                    )
                )
                output_markdown(
                    file_or_path, base_dir, output_file, iter_depth + 1
                )  # iteration

        else:  # is file
            # re to find target markdown files, $ for matching end of filename
            if is_markdown_file(filename):
                # or iter_depth != 0): # escape SUMMARY.md at base directory
                if filename not in [
                    "SUMMARY.md",
                    "0-README.md",
                    "README.md",
                ]:
                    # iter depth for indent, relpath and join to write link.
                    output_file.write(
                        "  " * iter_depth
                        + "* [{}]({})\n".format(
                            is_markdown_file(re.sub(r"^[0-9A-Z]+-", "", filename)),
                            os.path.join(
                                os.path.relpath(dir, base_dir).lstrip(r".\\"), filename
                            ),
                        )
                    )


def mdfile_in_dir(dir: str) -> bool:

    """
    Determine if there is markdown file in the directory
    """

    for _, _, files in os.walk(dir):
        for filename in files:
            if re.search(".md$|.markdown$", filename):
                return True
    return False


def is_markdown_file(filename: str) -> bool or str:

    """
    Determine if the file name is .md/.markdown

    i: filename
    o: filename without '.md' or '.markdown'
    """

    match = re.search(".md$|.markdown$", filename)
    if not match:
        return False
    elif len(match.group()) is len(".md"):
        return filename[:-3]
    elif len(match.group()) is len(".markdown"):
        return filename[:-9]


def createRead0(dir_input: str, filename: str):

    """
    Create a README index file in a subfolder
    """

    title = (
        re.sub(r".\\[0-9A-Z]+-", "", dir_input)
        if "\\" not in dir_input
        else re.sub(r".\\[0-9A-Z]+-", "", dir_input).split("\\")[-1]
    )
    readmeFile = open(os.path.join(dir_input, filename), "w")
    readmeFile.write(f"<!-- ex_nonav -->\n# {title}\n\n")
    output_markdown(dir_input, dir_input, readmeFile)

    print("createRead0 ", filename)  # output log


def sort_dir_file(listdir: str, dir: str) -> list:

    """
    use Pypi Project: cn-sort
    first files, then dirs
    first sort by pinyin, then by the stroke order
    """

    list_of_file = []
    list_of_dir = []

    for filename in listdir:
        if os.path.isdir(os.path.join(dir, filename)):
            list_of_dir.append(filename)
        else:
            list_of_file.append(filename)

    for dir in list_of_dir:
        list_of_file.append(dir)

    list_of_file = list(sort_text_list(list_of_file, mode=Mode.PINYIN))

    return list_of_file


def main():
    print(">> GitBook auto summary start <<")

    # output to flie
    output = open(os.path.join(".", "SUMMARY.md"), "w")
    output.write("# Summary\n\n")
    output.write("* [目录](./README.md)\n\n---\n\n")
    output_markdown(".", ".", output)
    output.close()

    print(">> GitBook auto summary finished:) <<")


if __name__ == "__main__":
    main()
