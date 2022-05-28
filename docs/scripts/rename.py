import os


def rename_file(folder_path, old, new):
    for path, subdirs, files in os.walk(folder_path):
        for name in files:
            if old in name:
                file_path = os.path.join(path, name)
                new_name = os.path.join(path, name.replace(old, new))
                os.rename(file_path, new_name)


def main():
    rename_file(".", "(", "（")
    rename_file(".", ")", "）")
    rename_file(".", " ", "、")


if __name__ == "__main__":
    main()
