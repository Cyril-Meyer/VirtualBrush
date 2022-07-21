import random
import time
import numpy as np
import skimage.draw
import skimage.io
import skimage.measure
import skimage.morphology
import skimage.transform
import matplotlib.pyplot as plt
import brush

fig, ax = plt.subplots()

FILENAME = 'LANDSCAPE'
EXT = '.jpg'
INPUT_IMAGE = skimage.io.imread(f'image/{FILENAME}{EXT}')[:, :, 0:3]
# padding to add to each border
PAD = 128
OUTPUT_IMAGE = np.zeros((INPUT_IMAGE.shape[0] + 2 * PAD, INPUT_IMAGE.shape[1] + 2 * PAD, 3), dtype=np.uint8)
OUTPUT_IMAGE.fill(255)
ANIM_COUNT = 1

def mean_absolute_error(X, Y):
    return np.mean(np.abs(X.astype(np.int64) - Y.astype(np.int64)))


def paint(n_segments, compactness, bristles_min, bristles_max, shape_disk_min_radius, shape_disk_max_radius):
    global ANIM_COUNT
    segments_slic = skimage.segmentation.slic(INPUT_IMAGE, n_segments=n_segments, compactness=compactness,
                                              sigma=1, start_label=1)
    '''
    plt.imshow(skimage.segmentation.mark_boundaries(INPUT_IMAGE, segments_slic))
    plt.show()
    '''
    regions = skimage.measure.regionprops(segments_slic, intensity_image=INPUT_IMAGE)

    for r in regions:
        # color
        color = r.mean_intensity
        # brushstroke movement
        convex_hull = skimage.morphology.convex_hull_object(r.image)
        skeleton = skimage.morphology.skeletonize(convex_hull)
        '''
        plt.imshow(skeleton)
        plt.show()
        '''
        # apply brushstroke
        argwhere = np.argwhere(skeleton > 0)
        x, y = argwhere[0]

        paintbrush = brush.random_paintbrush(position=[x, y],
                                             bristles_min=bristles_min, bristles_max=bristles_max,
                                             shape_disk_min_radius=shape_disk_min_radius,
                                             shape_disk_max_radius=shape_disk_max_radius)

        brushstroke_shape = (skeleton.shape[0] + PAD * 2, skeleton.shape[1] + PAD * 2)
        X = np.zeros(brushstroke_shape, dtype=np.uint8)
        i = 1
        old_x, old_y = argwhere[0]

        for x, y in argwhere[1:]:
            paintbrush.move([x - old_x, y - old_y])
            Y = np.zeros((brushstroke_shape[0], brushstroke_shape[1]), dtype=np.uint64)
            rr, cc = paintbrush.draw()
            rr, cc = np.array(rr), np.array(cc)
            rr += PAD
            cc += PAD
            rr = np.clip(rr, 0, Y.shape[0] - 1)
            cc = np.clip(cc, 0, Y.shape[1] - 1)
            Y[rr, cc] = 1

            Y = skimage.morphology.binary_dilation(Y, skimage.morphology.disk(2))
            X = X + Y
            old_x, old_y = x, y

        X = np.clip(X, 0, 255).astype(np.uint8)
        X = skimage.morphology.closing(X, skimage.morphology.disk(2))

        noise = np.random.normal(0, 1, (brushstroke_shape[0], brushstroke_shape[1]))
        X = np.where(X > 0, np.clip(X + noise, 0, 255), X).astype(np.uint8)

        # binary version
        X = (X > 10) * 1.0
        X = np.stack([X * color[0], X * color[1], X * color[2]], axis=-1).astype(np.uint8)
        OUTPUT_IMAGE[r.bbox[0]:r.bbox[2] + 2 * PAD, r.bbox[1]:r.bbox[3] + 2 * PAD] = \
            np.where(X > 0, X, OUTPUT_IMAGE[r.bbox[0]:r.bbox[2] + 2 * PAD, r.bbox[1]:r.bbox[3] + 2 * PAD])
        # intensity
        """
        I = np.copy(X).astype(np.uint64)
        I = np.clip(np.where(I > 0, I*5, I), 0, 255).astype(np.uint8)
        I = (I / I.max())
        I = np.stack([I, I, I], axis=-1)
        # value
        X = (X > 0) * 1.0
        X = np.stack([X * color[0], X * color[1], X * color[2]], axis=-1).astype(np.uint8)
        OUTPUT_IMAGE[r.bbox[0]:r.bbox[2]+2*PAD, r.bbox[1]:r.bbox[3]+2*PAD] =\
            np.where(X > 0, X * I + (1 - I) * OUTPUT_IMAGE[r.bbox[0]:r.bbox[2]+2*PAD, r.bbox[1]:r.bbox[3]+2*PAD],
                     OUTPUT_IMAGE[r.bbox[0]:r.bbox[2]+2*PAD, r.bbox[1]:r.bbox[3]+2*PAD])
        """

        skimage.io.imsave(f'animation/{FILENAME}_{str(ANIM_COUNT).zfill(8)}.png', OUTPUT_IMAGE[PAD:-PAD, PAD:-PAD])
        ANIM_COUNT += 1
    return


print('MAE', mean_absolute_error(INPUT_IMAGE, OUTPUT_IMAGE[PAD:-PAD, PAD:-PAD]))
t0 = time.time()

# fill segmentation region with large brushstroke
for n_segments in [5, 7, 10, 20, 40, 60, 80, 100, 125, 150, 175, 200, 250, 300, 350, 400, 450, 500]:
    for compactness in [12, 10]:
        paint(n_segments, compactness,
              bristles_min=20, bristles_max=40,
              shape_disk_min_radius=3, shape_disk_max_radius=6)
    print(n_segments, 'MAE', mean_absolute_error(INPUT_IMAGE, OUTPUT_IMAGE[PAD:-PAD, PAD:-PAD]))
    skimage.io.imsave(f'debug/{FILENAME}_{str(n_segments).zfill(4)}{EXT}', OUTPUT_IMAGE)

t1 = time.time()
print(t1 - t0, 's')

for n_segments in [550, 600, 700]:
    for compactness in [11, 9]:
        paint(n_segments, compactness,
              bristles_min=10, bristles_max=20,
              shape_disk_min_radius=1, shape_disk_max_radius=2)
        print('MAE', mean_absolute_error(INPUT_IMAGE, OUTPUT_IMAGE[PAD:-PAD, PAD:-PAD]))
    skimage.io.imsave(f'debug/{FILENAME}_{str(n_segments).zfill(4)}{EXT}', OUTPUT_IMAGE)

for n_segments in [700, 850, 1000]:
    for compactness in [10, 8]:
        paint(n_segments, compactness,
              bristles_min=5, bristles_max=10,
              shape_disk_min_radius=1, shape_disk_max_radius=2)
        print('MAE', mean_absolute_error(INPUT_IMAGE, OUTPUT_IMAGE[PAD:-PAD, PAD:-PAD]))
    skimage.io.imsave(f'debug/{FILENAME}_{str(n_segments).zfill(4)}{EXT}', OUTPUT_IMAGE)

t1 = time.time()
print(t1 - t0, 's')

# ims[0].save(f'result/{FILENAME}.gif', save_all=True, append_images=ims[1:])

plt.imshow(OUTPUT_IMAGE)
plt.show()
skimage.io.imsave(f'result/{FILENAME}{EXT}', OUTPUT_IMAGE)
