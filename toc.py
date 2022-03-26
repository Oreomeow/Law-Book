# -*- coding: utf-8 -*-

import argparse
import os
import re

from cn_sort.process_cn_word import *


def output_markdown(dire, base_dir, output_file, append, iter_depth=0):
    """Main iterator for get information from every file/folder

    i: directory, base directory(to calulate relative path),
       output file name, iter depth.
    p: Judge is directory or is file, then process .md/.markdown files.
    o: write .md information (with identation) to output_file.
    """
    ignores = ["_book", "docs", "images", "node_modules", "dict", ".git"]

    for filename in sort_dir_file(os.listdir(dire), base_dir):
        # add list and sort
        if filename in ignores:
            print("continue ", filename)  # output log
            continue

        print("Processing ", filename)  # output log
        file_or_path = os.path.join(dire, filename)
        if os.path.isdir(file_or_path):  # is dir
            if mdfile_in_dir(file_or_path):
                # if there is .md files in the folder, output folder name
                # output_file.write('  ' * iter_depth + '* ' + filename + '\n')
                createRead0(file_or_path, "0-README.md")
                output_file.write(
                    "  " * iter_depth
                    + "* [{}]({}/{})\n".format(
                        re.sub(r"^[0-9A-Z]+-", "", filename), filename, "0-README.md"
                    )
                )
                output_markdown(
                    file_or_path, base_dir, output_file, append, iter_depth + 1
                )  # iteration
        else:  # is file
            if is_markdown_file(filename):
                # re to find target markdown files, $ for matching end of filename
                if filename not in [
                    "SUMMARY.md",
                    "SUMMARY-GitBook-auto-summary.md",
                    "0-README.md",
                    "README.md",
                ]:
                    # or iter_depth != 0): # escape SUMMARY.md at base directory
                    output_file.write(
                        "  " * iter_depth
                        + "* [{}]({})\n".format(
                            write_md_filename(
                                re.sub(r"^[0-9A-Z]+-", "", filename), append
                            ),
                            os.path.join(
                                os.path.relpath(dire, base_dir).lstrip(r".\\"), filename
                            ),
                        )
                    )
                    # iter depth for indent, relpath and join to write link.


def mdfile_in_dir(dire):
    """判断目录中是否有MD文件"""
    for root, dirs, files in os.walk(dire):
        for filename in files:
            if re.search(".md$|.markdown$", filename):
                return True
    return False


def is_markdown_file(filename):
    """判断文件名是.Markdown

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


def createRead0(dir_input, filename):
    readmeFile = open(os.path.join(dir_input, filename), "w")
    title = re.sub(r"\.\\[0-9A-Z]+-", "", dir_input)
    readmeFile.write(f"<!-- ex_nonav -->\n# {title}\n\n")
    output_markdown(dir_input, dir_input, readmeFile, append=False)
    print("createRead0 ", filename)  # output log


def sort_dir_file(listdir, dire):
    # sort dirs and files, first files a-z, then dirs a-z
    list_of_file = []
    list_of_dir = []
    for filename in listdir:
        if os.path.isdir(os.path.join(dire, filename)):
            list_of_dir.append(filename)
        else:
            list_of_file.append(filename)
    for dire in list_of_dir:
        list_of_file.append(dire)

    list_of_file = list(sort_text_list(list_of_file, mode=Mode.PINYIN))
    return list_of_file


def write_md_filename(filename, append):
    """write markdown filename

    i: filename and append
    p: if append: find former list name and return
       else: write filename
    """
    if append:
        for line in former_summary_list:
            if re.search(filename, line):
                s = re.search("\[.*\]\(", line)
                return s.group()[1:-2]
        else:
            return is_markdown_file(filename)
    else:
        return is_markdown_file(filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--overwrite", help="overwrite on SUMMARY.md", action="store_true"
    )
    parser.add_argument(
        "-a", "--append", help="append on SUMMARY.md", action="store_true"
    )
    parser.add_argument("directory", help="the directory of your GitBook root")
    args = parser.parse_args()
    overwrite = args.overwrite
    append = args.append
    dir_input = args.directory

    # print information
    print("GitBook auto summary:", dir_input)
    if overwrite:
        print("--overwrite")
    if append and os.path.exists(os.path.join(dir_input, "SUMMARY.md")):
        # append: read former SUMMARY.md
        print("--append")
        global former_summary_list
        with open(os.path.join(dir_input, "SUMMARY.md")) as f:
            former_summary_list = f.readlines()
            f.close()
    print()
    # output to flie
    if overwrite == False and os.path.exists(os.path.join(dir_input, "SUMMARY.md")):
        # overwrite logic
        filename = "SUMMARY-GitBook-auto-summary.md"
    else:
        filename = "SUMMARY.md"
    output = open(os.path.join(dir_input, filename), "w")
    output.write("# Summary\n\n")
    output.write("* [目录](./README.md)\n\n---\n\n")
    output_markdown(dir_input, dir_input, output, append)
    output.close()
    print("GitBook auto summary finished:) ")
    return 0


if __name__ == "__main__":
    main()
