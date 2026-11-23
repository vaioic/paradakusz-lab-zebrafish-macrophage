from pathlib import Path

import tifffile

from shared import core

input_dir = Path("../data/2026-08-05 mpeg GA peptide/2026-08-05")

output_dir = Path("../data/2026-08-05 mpeg GA peptide/masks_2")
output_dir.mkdir(exist_ok=True, parents=True)

ims_file_list = list(input_dir.glob("Control*_5.ims"))

# ctr = 0
for file in ims_file_list:
    macrophage_img, protein_img = core.read_image(file)

    # core.preprocess_macrophage_image(
    #     macrophage_img,
    #     "../data/preprocessed/3.3 pg_uL GA peptide_2026-08-05_1.tiff",
    # )

    # import matplotlib.pyplot as plt
    # import skimage

    # cell_mask = skimage.filters.try_all_threshold(protein_img[0, :, :].squeeze())
    # plt.show()
    # exit()

    # cell_mask = core.segment_cells_3d(
    #     macrophage_img, mode="multiotsu", threshold_classes=4, threshold_value=1
    # )

    cell_mask = core.segment_cells_3d(macrophage_img, mode="minimum")
    tifffile.imwrite(output_dir / (file.stem + "_macrophage.tiff"), cell_mask)

    # spot_mask = core.segment_blobs(protein_img)
    # tifffile.imwrite(output_dir / (file.stem + "_protein.tiff"), spot_mask)

    # ctr += 1

    # if ctr > 2:
    #     break
