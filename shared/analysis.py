import re
from functools import reduce
from pathlib import Path

import pandas as pd


def analyze_imaris_output(data_dir):

    data_dir = Path(data_dir)

    # Define the output directory
    output_base_dir = data_dir / "Processed"
    output_base_dir.mkdir(parents=True, exist_ok=True)

    # Parse the folder structure
    macrophage_data_subdir = [
        p
        for p in data_dir.glob("*_Statistics")
        if p.is_dir() and not p.name.endswith("_protein_Statistics")
    ]

    if not macrophage_data_subdir:
        raise FileNotFoundError(f"Could not find statistics folder in {data_dir}")

    # print(macrophage_data_subdir)

    all_summary = []
    for p in macrophage_data_subdir:
        try:
            # Extract metadata
            conc, idx = parse_folder_name(p.name)

            if conc:
                conc = float(conc)
            else:
                conc = 0.0

            print(f"{p.name}: {conc}, {idx}")

            # Parse macrophage data
            df_volume = read_imaris_csv(p, "Volume")
            df_area = read_imaris_csv(p, "Area")
            df_protein_intensity = read_imaris_csv(p, "Intensity_Mean_Ch=2_Img=1")
            df_protein_overlap = read_imaris_csv(
                p, "Overlapped_Volume_to_Surfaces_Surfaces=Protein"
            )

            # df_merged = pd.concat(
            #     [df_volume, df_area, df_protein_overlap, df_protein_intensity],
            #     axis=1,
            #     join="outer",
            # ).reset_index()

            df_merged = reduce(
                lambda left, right: pd.merge(left, right, on="ID", how="outer"),
                [df_volume, df_area, df_protein_overlap, df_protein_intensity],
            )

            # Filter impossible volumes
            df_merged = df_merged[df_merged["Volume"] > 80]

            # print(df_merged)
            # exit()

            # print(df_merged)

            # Parse protein data
            protein_data_subdir = p.parent / p.name.replace(
                "_Statistics", "_protein_Statistics"
            )

            if not protein_data_subdir.is_dir():
                raise FileNotFoundError(
                    f"Protein data subdirectory {protein_data_subdir} not found."
                )

            df_protein_volume = read_imaris_csv(protein_data_subdir, "Volume")
            df_protein_intensity = read_imaris_csv(
                protein_data_subdir, "Intensity_Mean_Ch=2_Img=1"
            )

            df_protein_merged = reduce(
                lambda left, right: pd.merge(left, right, on="ID", how="outer"),
                [
                    df_protein_volume,
                    df_protein_intensity,
                ],
            )

            # print(df_protein_merged)

            # Write data
            df_merged.to_csv(output_base_dir / f"{p.name}_macrophage.csv", index=False)
            df_protein_merged.to_csv(
                output_base_dir / f"{p.name}_protein.csv", index=False
            )

            # ---Calculate summary statistics---

            summary_stats = {
                "Image": p.name.replace("_Statistics", ""),
                "Concentration": conc,
                "Replicate": int(idx) + 1,
                "Num macrophages": len(df_merged),
                "Average macrophage volume": df_merged["Volume"].mean(),
                "StDev macrophage volume": df_merged["Volume"].std(),
                "Average protein volume": df_protein_merged["Volume"].mean(),
                "StDev protein volume": df_protein_merged["Volume"].std(),
                "Average protein intensity": df_protein_merged["Intensity Mean"].mean(),
                "StDev protein intensity": df_protein_merged["Intensity Mean"].std(),
                "Total protein volume": df_protein_merged["Volume"].sum(),
                "Protein volume inside macrophage": df_merged["Protein Volume"].sum(),
                "Protein volume outside macrophage": df_protein_merged["Volume"].sum()
                - df_merged["Protein Volume"].sum(),
            }

            all_summary.append(summary_stats)
        except FileNotFoundError as e:
            print(f"{p.name} missing data: {e}")

    # Write data
    df_summary = pd.DataFrame(all_summary)
    df_summary.to_csv(output_base_dir / "summary.csv", index=False)

    # Macrophage morphology (area, circularity, elongation, branching?)
    # red fluorescent signal inside macrophages (vesicle size, intensity per cell)
    # red signal outside macrophages


def read_imaris_csv(folder: Path, name: str):

    csv_file = list(folder.glob(f"*_{name}.csv"))

    if not csv_file:
        raise FileNotFoundError(
            f"Could not find file matching '*_{name}.csv' in {folder}."
        )

    # Skip Imaris headers
    df = pd.read_csv(csv_file[0], skiprows=3)

    # Remove "Unanamed" columns caused by trailing commas
    df = df.loc[:, ~df.columns.str.startswith("Unnamed:") | df.notna().any()]

    # Clean up column names
    if "Unit" in df.columns:
        df = df.rename(columns={"Unit": f"{name}_Unit"})

    if (
        name == "Overlapped_Volume_to_Surfaces_Surfaces=Protein"
        and "Overlapped Volume to Surfaces" in df.columns
    ):
        df = df.rename(
            columns={
                "Overlapped Volume to Surfaces": "Protein Volume",
                f"{name}_Unit": "Protein Volume_Unit",
            }
        )

    if name == "Intensity_Mean_Ch=2_Img=1" and "Intensity Mean" in df.columns:
        df = df.drop(columns=[f"{name}_Unit", "Channel", "Image"])

    # Drop unwanted columns
    df = df.drop(columns=["Category", "Time", "Surfaces"], errors="ignore")
    df.set_index("ID")

    # print(df)

    return df


def parse_folder_name(name):

    pattern = re.compile(
        r"^(?:(?P<conc>[\d.]+)\s+pg_uL\b.*|Control)_\d{4}-\d{2}-\d{2}(?:_(?P<idx>\d+))?_Statistics$"
    )

    # Note: Returns None if group is Control

    m = pattern.match(name)
    if not m:
        raise ValueError(f"Unexpected folder name: {name}")

    return m.group("conc"), m.group("idx") or "0"
