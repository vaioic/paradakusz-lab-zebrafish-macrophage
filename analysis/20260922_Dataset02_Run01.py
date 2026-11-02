# Dataset 02
# ----------
#  * 2026-07-29 mpeg GA peptide
#  * 2026-08-05 mpeg GA peptide

from shared import core

core.analyze_images_in_dir(
    r"../data/Dataset02/2026-07-29 mpeg GA peptide/2026-07-29",
    r"../processed/20260923 Dataset02_A",
)

core.analyze_images_in_dir(
    r"../data/Dataset02/2026-08-05 mpeg GA peptide/2026-08-05",
    r"../processed/20260923 Dataset02_B",
)
