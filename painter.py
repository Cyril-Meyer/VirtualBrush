import random
import time
import numpy as np
import skimage.draw
import skimage.io
import skimage.measure
import skimage.morphology
import matplotlib.pyplot as plt
import brush

FILENAME = 'INFERNO.png'
INPUT_IMAGE = skimage.io.imread(f'image/{FILENAME}')[:, :, 0:3]
OUTPUT_IMAGE = np.zeros(INPUT_IMAGE.shape, dtype=np.uint8)
OUTPUT_IMAGE.fill(255)

t0 = time.time()
# fill segmentation region with large brushstroke
for n_segments in [5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 250, 300, 350, 400, 450, 500]:
    for compactness in [6, 10]:
        segments_slic = skimage.segmentation.slic(INPUT_IMAGE, n_segments=n_segments, compactness=compactness, sigma=1, start_label=1)
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
            # todo : fix error when negative draw id (add padding / check values ?)
            argwhere = np.argwhere(skeleton > 0)
            x, y = argwhere[0]

            paintbrush = brush.random_paintbrush(position=[x, y],
                                           bristles_min=25, bristles_max=50,
                                           shape_disk_min_radius=3, shape_disk_max_radius=5)

            X = np.zeros(skeleton.shape, dtype=np.uint8)
            i = 1
            old_x, old_y = argwhere[0]

            for x, y in argwhere[1:]:
                paintbrush.move([x - old_x, y - old_y])
                Y = np.zeros((skeleton.shape[0], skeleton.shape[1]), dtype=np.uint64)

                try:
                    Y[paintbrush.draw()] = 1
                except Exception as e:
                    # print(e)
                    pass
                Y = skimage.morphology.binary_dilation(Y, skimage.morphology.disk(2))
                X = X + Y
                old_x, old_y = x, y

            X = np.clip(X, 0, 255).astype(np.uint8)
            X = skimage.morphology.closing(X, skimage.morphology.disk(2))

            noise = np.random.normal(0, 1, (skeleton.shape[0], skeleton.shape[1]))
            X = np.where(X > 0, np.clip(X + noise, 0, 255), X).astype(np.uint8)
            # todo remove this simplification and use non binary brushstroke
            X = (X > 10) * 1.0
            X = np.stack([X * color[0], X * color[1], X * color[2]], axis=-1).astype(np.uint8)

            OUTPUT_IMAGE[r.bbox[0]:r.bbox[2],r.bbox[1]:r.bbox[3]] =\
                np.where(X > 0, X, OUTPUT_IMAGE[r.bbox[0]:r.bbox[2],r.bbox[1]:r.bbox[3]])

    skimage.io.imsave(f'result/{str(n_segments).zfill(4)}_{FILENAME}', OUTPUT_IMAGE)

t1 = time.time()
print(t1 - t0, 's')

plt.imshow(OUTPUT_IMAGE)
plt.show()
skimage.io.imsave(f'result/{FILENAME}', OUTPUT_IMAGE)
