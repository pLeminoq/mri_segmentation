import os
import subprocess
import tempfile

import SimpleITK as sitk

from .util import read_image

def segment(sitk_mri: sitk.Image, subsets = None, fast = None) -> dict[str, sitk.Image]:
    with tempfile.TemporaryDirectory() as tmpdir:
        nifty_mri = os.path.join(tmpdir, "mri.nii.gz")
        sitk.WriteImage(sitk_mri, nifty_mri)

        dir_segmentation = os.path.join(tmpdir, "segmentation")
        os.mkdir(dir_segmentation)

        
        args = ["TotalSegmentator", "-i", nifty_mri, "-o", dir_segmentation, "--task", "total_mr"]
        if fast:
            args.append(f"--fast")
        if subsets is not None:
            args.append("--roi_subset")
            args.extend(subsets)

        subprocess.run(args)
        
        segmentations = {}
        for filename in os.listdir(dir_segmentation):
            if not filename.endswith(".nii.gz"):
                continue

            _filename = os.path.join(dir_segmentation, filename)
            mask_name = os.path.basename(_filename).split(".")[0]
            segmentations[mask_name] = read_image(_filename)
    return segmentations

def segment_liver(sitk_mri, fast=None):
    return segment(sitk_mri, subsets=["liver"], fast=fast)["liver"]

if __name__ == "__main__":
    import os
    os.environ["TOTALSEG_HOME_DIR"] = os.path.join(os.getcwd(), ".totalsegmentator")
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("mri")
    args = parser.parse_args()

    sitk_mri = read_image(args.mri)
    segments = segment_liver(sitk_mri)
