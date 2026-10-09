# import os
# import zipfile
# import shutil

# zip_path = 'datasets/Grasp-Anything/grasp_label_positive.zip'

# with zipfile.ZipFile(zip_path, 'r') as zf:
#         all_files = zf.namelist()
#         for x in all_files[:10]:
#                 print(x)

import zipfile

zips = {
    'scene_description': 'datasets/Grasp-Anything/scene_description.zip',
    'grasp_label_negative': 'datasets/Grasp-Anything/grasp_label_negative.zip',
    'mask': 'datasets/Grasp-Anything/mask.zip',
}

for name, path in zips.items():
    with zipfile.ZipFile(path, 'r') as zf:
        files = zf.namelist()
        print(f"\n--- {name} ---")
        for f in files[:5]:
            print(f)


##### read a pkl file

# import pickle

# with open('datasets/Grasp-Anything/sample/scene_description/0000ad2a7e20638385adbf6d46d660303480059faa55cf0caca0e05643c5f9b6.pkl', 'rb') as f:
#     data = pickle.load(f)

# print(type(data))
# print(len(data))
# print(list(data)[:10])  # first 10 entries
