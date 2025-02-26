import os

import numpy as np
from numpy.typing import NDArray
import SimpleITK as sitk


def read_image(filename: str) -> sitk.Image:
    if os.path.isdir(filename):
        sitk_reader = sitk.ImageSeriesReader()
        sitk_reader.SetFileNames(sitk_reader.GetGDCMSeriesFileNames(filename))
    else:
        sitk_reader = sitk.ImageFileReader()
        sitk_reader.SetFileName(filename)
    return sitk_reader.Execute()


def window(image: NDArray, center: float, width: float) -> NDArray:
    width_h = width / 2.0
    return np.clip(image, a_min=center - width_h, a_max=center + width_h)


def normalize(img: NDArray) -> NDArray:
    _max = img.max()
    _min = img.min()

    # special case all zeroes
    if _max == _min:
        return img

    return (img - _min) / (_max - _min)

def to_grayscale(img: NDArray) -> NDArray:
    return (img * 255).astype(np.uint8)

