import numpy as np
import skimage.segmentation
import cv2

WNAME = 'VirtualBrush - painter gui'


def show_input_image():
    global DATA
    DATA = np.copy(INPUT_IMAGE)[:, :, ::-1]


def show_output_image():
    pass


def show_segmentation():
    global DATA
    n_segments = cv2.getTrackbarPos('n_segments', WNAME)
    compactness = cv2.getTrackbarPos('compactness', WNAME) / 100 + 1e-9

    segments_slic = skimage.segmentation.slic(INPUT_IMAGE, n_segments=n_segments, compactness=compactness,
                                              sigma=1, start_label=1)

    DATA.fill(0)
    DATA = skimage.segmentation.mark_boundaries(INPUT_IMAGE, segments_slic)[:, :, ::-1]


def paint():
    pass


cv2.namedWindow(WNAME, cv2.WINDOW_NORMAL)
cv2.createTrackbar('n_segments', WNAME, 1, 1000, lambda x: None)
cv2.createTrackbar('compactness', WNAME, 0, 1000, lambda x: None)

FILENAME = 'LANDSCAPE'
EXT = '.jpg'
INPUT_IMAGE = skimage.io.imread(f'image/{FILENAME}{EXT}')[:, :, 0:3]
DATA = INPUT_IMAGE
show_input_image()

while True:
    cv2.imshow(WNAME, DATA)
    c = cv2.waitKey(20) & 0xFF
    if c == 27:
        break
    if c == ord('a'):
        show_input_image()
    elif c == ord('z'):
        show_output_image()
    elif c == ord('e'):
        show_segmentation()
    elif c == ord('r'):
        paint()

cv2.destroyAllWindows()
