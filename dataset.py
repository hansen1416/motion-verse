# import os
# import json
# import pathlib
# from typing import List

# BASE_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "motionx")


# def read_motion_keypoints():

#     local_path = os.path.join(BASE_DIR, "motion", "keypoints", "animation")

#     # # list all files in the folder
#     # all_files: List[str] = os.listdir(local_path)

#     # print(all_files)

#     # get all files in the folder recursively
#     all_files: List[str] = [
#         str(f) for f in pathlib.Path(local_path).rglob("*") if f.is_file()
#     ]

#     for filepath in all_files:
#         with open(filepath, "r") as f:
#             data = json.load(f)

#         break

#     print(data.keys())


# if __name__ == "__main__":
#     read_motion_keypoints()
import os
import numpy as np
import torch

# read motion and save as smplx representation
motion = np.load(
    os.path.join(
        os.path.expanduser("~"),
        "Downloads",
        "motionx",
        "motion",
        "motion_generation",
        "smplx322",
        "animation",
        "animation",
        "Ways_to_Catch_360_clip1.npy",
    )
)

motion = torch.tensor(motion).float()
motion_parms = {
    "root_orient": motion[:, :3],  # controls the global root orientation
    "pose_body": motion[:, 3 : 3 + 63],  # controls the body
    "pose_hand": motion[:, 66 : 66 + 90],  # controls the finger articulation
    "pose_jaw": motion[:, 66 + 90 : 66 + 93],  # controls the yaw pose
    "face_expr": motion[:, 159 : 159 + 50],  # controls the face expression
    "face_shape": motion[:, 209 : 209 + 100],  # controls the face shape
    "trans": motion[:, 309 : 309 + 3],  # controls the global body position
    "betas": motion[:, 312:],  # controls the body shape. Body shape is static
}

# for k, v in motion_parms.items():
# print(k, v.shape)
# root_orient torch.Size([90, 3])
# pose_body torch.Size([90, 63])
# pose_hand torch.Size([90, 90])
# pose_jaw torch.Size([90, 3])
# face_expr torch.Size([90, 50])
# face_shape torch.Size([90, 100])
# trans torch.Size([90, 3])
# betas torch.Size([90, 10])


# # read text labels
# semantic_text = np.loadtxt(
#     os.path.join(
#         os.path.expanduser("~"),
#         "Downloads",
#         "motionx",
#         "text",
#         "semantic_label",
#         "animation",
#         "animation",
#         "Ways_to_Catch_360_clip1.txt",
#     )
# )  # semantic labels


# print(semantic_text)
