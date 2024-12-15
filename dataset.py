import os
import json
import pathlib
from typing import List

BASE_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "motionx")


def read_motion_keypoints():

    local_path = os.path.join(BASE_DIR, "motion", "keypoints", "animation")

    # # list all files in the folder
    # all_files: List[str] = os.listdir(local_path)

    # print(all_files)

    # get all files in the folder recursively
    all_files: List[str] = [
        str(f) for f in pathlib.Path(local_path).rglob("*") if f.is_file()
    ]

    for filepath in all_files:
        with open(filepath, "r") as f:
            data = json.load(f)

        break

    print(data.keys())


if __name__ == "__main__":
    read_motion_keypoints()
