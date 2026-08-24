# OIC-264

The goal of this project is to quantify zebrafish macrophage biology following phagocytosis of an RFP protein cargo in the caudal hematopoietic tissue. In the dataset for this project, macrophages are labeled in green and the toxic protein is tagged with an RFP to study its uptake and degradation. Currently, the dataset is of single images captured at the same time post exposure.

The goal is to establish a robust and reproducible pipeline capable of extracting the following quantitative parameters:

1. Macrophage morphology / activation profile - Measurements of cell shape descriptors (area, circularity, elongation, branching, etc.) to assess activation state.
2. Intracellular protein load - Quantification of red fluorescent signal contained within macrophages, including vesicle number, size, and intensity per cell.
3. Extracellular protein load - Quantification of red fluorescent signal outside macrophages within the CHT region to estimate non-phagocytosed material.

This project is in active development and things might change rapidly.


## Usage

### Setup and installation

#### Using uv (Recommended)

This project uses [uv](https://docs.astral.sh/uv/) to manage virtual environments and dependencies. 

1. Install ``uv``
    * **macOS or Linux:** ``curl -LsSf https://astral.sh/uv/install.sh | sh``
    * **Windows:** ``powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"``
    
    To check if you have ``uv`` installed, open a terminal and run ``uv --version``.

2. Clone the repository
   ```bash
   git clone git@github.com:vaioic/paradakusz-lab-zebrafish-macrophage.git
   cd paradakusz-lab-zebrafish-macrophage
   ```

3. Sync the environment (this will setup the correct virtual environment and dependencies)
   ```bash
   uv sync
   ```

4. Run the analysis
   ```bash
   uv run analysis/analysis_script.py
   ```

#### Using venv and pip

1. Clone the repository
   ```bash
   git clone git@github.com:vaioic/paradakusz-lab-zebrafish-macrophage.git
   cd paradakusz-lab-zebrafish-macrophage
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   ```

3. Activate the environment
   ```bash
   # macOS/Linux
   source ./venv/bin/activate

   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   ```

4. Install the repository as an editable module
   ```bash
   python -m pip install -e .
   ```

5. Run the analysis script
   ```bash
   python -m analysis.analysis_script

   # or
   python analysis/analysis_script.py
   ```

## Analysis

To analyze images, call the ``analyze_images`` script. The script takes two input arguments: a string containing the path to an image or a directory containing images, and the path to the output directory.

   Example:
   ```bash
   python -m python -m analyze_images "../data/2026-02-13" "../processed/output"
   ```

### Output files

The script will generate the following files:

1.	``results.csv`` – This is the data per cell for all the images that were processed.

2.	``summary.csv`` – This contains image-wide data (Number of cells, Total Cell Volume, Total Protein Volume inside Cell, Total Protein Volume outside Cell)

3.	TIFF files showing segmentation results. Each file is a z-stack that can be viewed using Fiji/ImageJ.

   -	Individual cells are outlined in yellow and should have an ID number (corresponding to the “Cell ID” in the results.csv). Note that I ended up performing the analysis in 3D so the same cell should be visible in multiple planes.

   -	Protein clusters are labeled with a cyan outline.

## Issues

If you encounter any issues with running the code or have any questions, please create an [Issue](https://github.com/vaioic/paradakusz-lab-zebrafish-macrophage/issues) or send an email to opticalimaging@vai.org. If you are reporting a bug, please include any error messages to aid with troubleshooting.

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.

## Citing & Acknowledgements

This repository is publicly available for open-source use, but it is developed and maintained by the Optical Imaging Core at the Van Andel Institute. If code from this repository contributed to data used in a publication, abstract, or presentation, please cite and acknowledge our work based on your affiliation:

### For External Users
Please cite this repository and acknowledge the author(s) in your publication's materials, methods, or acknowledgements section:
> "Image analysis pipelines were adapted from open-source tools developed by the Optical Imaging Core at the Van Andel Institute (GitHub:[paradakusz-lab-zebrafish-macrophage](https://github.com/vaioic/paradakusz-lab-zebrafish-macrophage))."

If you require custom adjustments or advanced analysis support, please contact us at opticalimaging@vai.org.

### For Internal Users & Close Collaborators
If you are an internal researcher or an external collaborator working directly with our staff, please include our Research Resource Identifier (RRID) in your materials and methods section:
> "Image analysis and data processing were performed in collaboration with the Optical Imaging Core at the Van Andel Institute (RRID:SCR_021968)."

Please review the Acknowledgement and Authorship Guidelines on [VAI's Core Technology and Services website](https://vanandelinstitute.sharepoint.com/sites/Cores/SitePages/Acknowledgements-and-Authorship.aspx)

### Contributors
<a href="https://github.com/vaioic/paradakusz-lab-zebrafish-macrophage/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=vaioic/paradakusz-lab-zebrafish-macrophage" />
</a>

## Changelog

### v0.1.0 (2026-03-19)
* Initial commit with preliminary code ([OIC-264](https://varioic.atlassian.net/browse/OIC-264))