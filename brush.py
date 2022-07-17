import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import skimage.draw
import skimage.morphology


def normalize(v):
    return v / np.sqrt(np.sum(v**2))


class Bristle:
    def __init__(self, length=400, initial_direction=[1, 0]):
        assert length > 0
        assert len(initial_direction) == 2
        initial_direction = np.array(initial_direction)
        self.length = length
        self.p0 = np.array([0, 0], dtype=np.uint8)
        self.p2 = normalize(initial_direction) * self.length
        self.p1 = 0.5 * self.p2 + 0.5 * self.p0

    def next(self, direction, w=0.25, rigidity=0.5):
        direction = np.array(direction)
        p2 = normalize(w * normalize(self.p2) + (1 - w) * direction) * self.length
        p2_vector = p2 - self.p2
        self.p1 = 0.5 * self.p2 + 0.5 * self.p0
        self.p2 = normalize(self.p2 + p2_vector * rigidity) * self.length


    def draw(self):
        # return skimage.draw.line(0, 0, round(self.p2[0]), round(self.p2[1]))
        return skimage.draw.bezier_curve(0, 0,
                                         round(self.p1[0]), round(self.p1[1]),
                                         round(self.p2[0]), round(self.p2[1]),
                                         1)


class Paintbrush:
    def __init__(self):
        self.bristles = []
        self.bristles.append(Bristle())


def plot_bristle(bristle):
    X = np.zeros((512, 512), dtype=np.uint8)
    rr, cc = bristle.draw()
    X[rr, cc] = 255
    X = skimage.morphology.binary_dilation(X, skimage.morphology.disk(5))
    plt.imshow(X, cmap='gray', interpolation='nearest')
    plt.gca().invert_yaxis()
    plt.show()


def plot_bristle_animated(bristle, ax):
    X = np.zeros((512, 512), dtype=np.uint8)
    rr, cc = bristle.draw()
    X[rr, cc] = 255
    X = skimage.morphology.binary_dilation(X, skimage.morphology.disk(5))
    im = ax.imshow(X, cmap='gray', interpolation='nearest', animated=True)
    return im


if __name__ == "__main__":
    fig, ax = plt.subplots()
    ims = []

    b = Bristle()
    ims.append([plot_bristle_animated(b, ax)])
    for x in range(5):
        b.next([0, 1])
        ims.append([plot_bristle_animated(b, ax)])
    for x in range(5):
        b.next([1, 0])
        ims.append([plot_bristle_animated(b, ax)])
    for x in range(10):
        b.next([1, 1])
        ims.append([plot_bristle_animated(b, ax)])

    ani = animation.ArtistAnimation(fig, ims, interval=250, blit=True,
                                    repeat_delay=1000)
    plt.show()
