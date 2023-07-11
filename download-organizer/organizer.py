import os

exts = {
    "audio": (
        ".3ga",
        ".aac",
        ".ac3",
        ".aif",
        ".aiff",
        ".alac",
        ".amr",
        ".ape",
        ".au",
        ".dss",
        ".flac",
        ".flv",
        ".m4a",
        ".m4b",
        ".m4p",
        ".mp3",
        ".mpga",
        ".ogg",
        ".oga",
        ".mogg",
        ".opus",
        ".qcp",
        ".tta",
        ".voc",
        ".wav",
        ".wma",
        ".wv",
    ),
    "video": (".webm", ".MTS", ".M2TS", ".TS", ".mov", ".mp4", ".m4p", ".m4v", ".mxf"),
    "img": (
        ".jpg",
        ".jpeg",
        ".jfif",
        ".pjpeg",
        ".pjp",
        ".png",
        ".gif",
        ".webp",
        ".svg",
        ".apng",
        ".avif",
    ),
    "docs": (".docx", ".pdf", ".csv", ".xlsx", ".txt"),
}


def get_all_files_from_dir(dir_name="."):
    return os.listdir(dir_name)


def split_files(files):
    splited = {"audio": [], "video": [], "img": [], "docs": [], "other": []}
    for file in files:
        if file == "organizer.py":
            continue
        if os.path.isdir(file):
            continue
        ext = os.path.splitext(file)[-1].lower()
        for key in exts:
            if ext in exts[key]:
                splited[key].append(file)
                break
        else:
            splited["other"].append(file)
    return splited


def create_dirs(dir_name):
    dirs = ["img", "video", "audio", "docs", "other"]
    for dir in dirs:
        if not os.path.exists(dir_name + f"/{dir}"):
            os.makedirs(dir_name + f"/{dir}")


def move_files(files_dict, dir_name):
    for category in files_dict:
        for file in files_dict[category]:
            new_file = f"{dir_name}/{category}/{file}"
            while os.path.isfile(new_file):
                name, ext = os.path.splitext(new_file)
                new_file = name + " copy" + ext

            os.replace(f"{dir_name}/{file}", new_file)


if __name__ == "__main__":
    directory = "./download-organizer"
    files = get_all_files_from_dir(directory)
    d = split_files(files)
    create_dirs(directory)
    move_files(d, directory)
