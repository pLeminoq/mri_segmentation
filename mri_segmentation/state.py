import cv2 as cv
import numpy as np
import SimpleITK as sitk
from reacTk.decorator import asynchron
from reacTk.widget.canvas.image import ImageData
from widget_state import (
    BoolState,
    HigherOrderState,
    NumberState,
    ObjectState,
    StringState,
    computed,
)

from .total_segmentator import segment_liver
from .util import read_image, normalize, window, to_grayscale


class AppState(HigherOrderState):

    def __init__(self):
        super().__init__()

        self.mri_dir = StringState("")
        self.sitk_mask = ObjectState(sitk.Image(self.sitk_mri.value.GetSize(), sitk.sitkFloat64))
        self.sitk_mri.on_change(lambda _: self.compute_mask(), trigger=True)

        self.loop = BoolState(False)
        self.slice = NumberState(0)
        self.window_center = NumberState(0)
        self.window_width = NumberState(0)

        self._validate_computed_states()

        self.mri.on_change(lambda _: self.reset_params(), trigger=True)

    def reset_params(self):
        self.slice.value = 0
        self.window_width.value = self.mri.value.max() - self.mri.value.min()
        self.window_center.value = self.window_width.value / 2.0

    @asynchron 
    def compute_mask(self):
        if sitk.GetArrayFromImage(self.sitk_mri.value).max() == 0.0:
            return
        self.sitk_mask.value = segment_liver(self.sitk_mri.value)

    @computed
    def sitk_mri(self, mri_dir: StringState) -> ObjectState:
        if mri_dir.value == "":
            return ObjectState(sitk.Image((512, 512, 32), sitk.sitkFloat64))
        return ObjectState(read_image(mri_dir.value))

    @computed
    def mri(self, sitk_mri: ObjectState) -> ObjectState:
        return ObjectState(sitk.GetArrayFromImage(sitk_mri.value))

    @computed
    def mri_norm(
        self, mri: ObjectState, window_center: NumberState, window_width: NumberState
    ) -> ObjectState:
        return ObjectState(
            to_grayscale(
                normalize(window(mri.value, window_center.value, window_width.value))
            )
        )

    @computed
    def mri_slice(self, mri_norm: ObjectState, slice: NumberState) -> ImageData:
        return ImageData(mri_norm.value[slice.value])

    @computed
    def mask(self, sitk_mask: ObjectState) -> ObjectState:
        return ObjectState(sitk.GetArrayFromImage(sitk_mask.value > 0.0))

    @computed
    def mask_slice(self, mask: ObjectState, slice: NumberState) -> ImageData:
        return ImageData(to_grayscale(mask.value[slice.value]))

    @computed
    def slice_image(self, mri_slice: ImageData, mask_slice: ImageData) -> ImageData:
        img = mri_slice.value
        img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)

        mask = mask_slice.value
        mask = mask.reshape(*mask.shape, -1)
        color = np.array([0, 200, 0], np.uint8)
        color = color.reshape(1, 1, -1)
        mask = mask * color

        if not((np.array(mask.shape) == np.array(img.shape)).all()):
            mask = cv.resize(mask, img.shape[:2][::-1])

        res = cv.addWeighted(img, 1.0, mask, 0.3, 0.0)

        return ImageData(res)

    @computed
    def volume(self, sitk_mri, mask):
        pixel_volume = np.product(sitk_mri.value.GetSpacing())
        volume = mask.value.sum() * pixel_volume
        return NumberState(volume / 1000000) 


app_state = AppState()
