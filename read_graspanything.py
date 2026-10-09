import os
import zipfile

#  Config 
IMAGE_DIR   = 'datasets/Grasp-Anything/image/'
OUTPUT_BASE = 'datasets/Grasp-Anything/sample/'

ZIP_FILES = {
    'scene_description':    'datasets/Grasp-Anything/scene_description.zip',
    'grasp_label_positive': 'datasets/Grasp-Anything/grasp_label_positive.zip',
    'grasp_label_negative': 'datasets/Grasp-Anything/grasp_label_negative.zip',
    'mask':                 'datasets/Grasp-Anything/mask.zip',
}

# Folders that use {hash}_{n}.ext pattern
MULTI_OBJECT_FOLDERS = {'grasp_label_positive', 'grasp_label_negative', 'mask'}

#  Get selected stems from your 50 images 
selected_stems = set(
    os.path.splitext(f)[0]
    for f in os.listdir(IMAGE_DIR)
    if f.endswith('.jpg')
)
print(f"Selected stems: {len(selected_stems)}")


os.makedirs(os.path.join(OUTPUT_BASE, "scene_description"), exist_ok=True)
with zipfile.ZipFile('datasets/Grasp-Anything/scene_description.zip', 'r') as zf:
    count = 0
    for filepath in zf.namelist():
        filename = os.path.basename(filepath)
        if not filename:
            continue
        hash_stem = os.path.splitext(filename)[0]
        if hash_stem in selected_stems:
            count += 1
            data = zf.read(filepath)
            out_path = os.path.join(OUTPUT_BASE, "scene_description", filename)
            with open(out_path, 'wb') as out_f:
                out_f.write(data)
    print("saved", count, "scene_description files")


os.makedirs(os.path.join(OUTPUT_BASE, "grasp_label_positive"), exist_ok=True)
with zipfile.ZipFile('datasets/Grasp-Anything/grasp_label_positive.zip', 'r') as zf:
    count = 0
    for filepath in zf.namelist():
        filename = os.path.basename(filepath)
        if not filename:
            continue
        stem_no_ext = os.path.splitext(filename)[0]
        hash_stem = stem_no_ext.rsplit('_', 1)[0]

        if hash_stem in selected_stems:
            count += 1
            data = zf.read(filepath)
            out_path = os.path.join(OUTPUT_BASE, "grasp_label_positive", filename)
            with open(out_path, 'wb') as out_f:
                out_f.write(data)

    print("saved", count, "grasp_label_positive files")


os.makedirs(os.path.join(OUTPUT_BASE, "grasp_label_negative"), exist_ok=True)
with zipfile.ZipFile('datasets/Grasp-Anything/grasp_label_negative.zip', 'r') as zf:
    count = 0
    for filepath in zf.namelist():
        filename = os.path.basename(filepath)
        if not filename:
            continue
        stem_no_ext = os.path.splitext(filename)[0]
        hash_stem = stem_no_ext.rsplit('_', 1)[0]

        if hash_stem in selected_stems:
            count += 1
            data = zf.read(filepath)
            out_path = os.path.join(OUTPUT_BASE, "grasp_label_negative", filename)
            with open(out_path, 'wb') as out_f:
                out_f.write(data)

    print("saved", count, "grasp_label_negative files")


os.makedirs(os.path.join(OUTPUT_BASE, "mask"), exist_ok=True)
with zipfile.ZipFile('datasets/Grasp-Anything/mask.zip', 'r') as zf:
    count = 0
    for filepath in zf.namelist():
        filename = os.path.basename(filepath)
        if not filename:
            continue
        stem_no_ext = os.path.splitext(filename)[0]
        hash_stem = stem_no_ext.rsplit('_', 1)[0]

        if hash_stem in selected_stems:
            count += 1
            data = zf.read(filepath)
            out_path = os.path.join(OUTPUT_BASE, "mask", filename)
            with open(out_path, 'wb') as out_f:
                out_f.write(data)

    print("saved", count, "mask files")

