import random
import numpy as np
import skimage.draw
import skimage.morphology
import matplotlib.pyplot as plt


def normalize(v):
    return v / np.sqrt(np.sum(v**2))


class Bristle:
    def __init__(self, length=100, rigidity=0.1, initial_direction=[1, 0]):
        assert length > 0
        assert 0 < rigidity <= 1
        assert len(initial_direction) == 2
        assert np.sum(initial_direction) != 0
        initial_direction = np.array(initial_direction)
        self.length = length
        self.rigidity = rigidity
        self.p0 = np.array([0, 0], dtype=np.uint8)
        self.p2 = normalize(initial_direction) * self.length
        self.p1 = 0.5 * self.p2 + 0.5 * self.p0

    def next(self, direction, w=0.05):
        direction = np.array(direction)
        p2 = normalize(w * normalize(self.p2) + (1 - w) * direction) * self.length
        p2_vector = p2 - self.p2
        old_p1 = self.p1
        self.p1 = 0.5 * self.p2 + 0.5 * self.p0
        p1_noise = random.uniform(0.0, 0.25)
        self.p1 = (1 - p1_noise) * self.p1 + p1_noise * old_p1
        self.p2 = normalize(self.p2 + p2_vector * self.rigidity) * self.length
        # symmetry
        self.p1 = self.p1 + (0.5 * self.p2 + 0.5 * self.p0) - self.p1 + (0.5 * self.p2 + 0.5 * self.p0) - self.p1

    def draw(self, origin):
        # return skimage.draw.line(0, 0, round(self.p2[0]), round(self.p2[1]))
        return skimage.draw.bezier_curve(round(origin[0]),
                                         round(origin[1]),
                                         round(origin[0] + self.p1[0]),
                                         round(origin[1] + self.p1[1]),
                                         round(origin[0] + self.p2[0]),
                                         round(origin[1] + self.p2[1]),
                                         1)


def random_bristle(length_min=25, length_max=50,
                   rigidity_min=0.1, rigidity_max=0.2,
                   initial_direction=[0, 0], initial_direction_epsilon=0.1):

    length = random.randint(length_min, length_max)
    rigidity = random.uniform(rigidity_min, rigidity_max)
    epsilon_x = random.uniform(-initial_direction_epsilon, initial_direction_epsilon)
    epsilon_y = random.uniform(-initial_direction_epsilon, initial_direction_epsilon)
    initial_direction[0] += epsilon_x
    initial_direction[1] += epsilon_y

    bristle = Bristle(length=length,
                      rigidity=rigidity,
                      initial_direction=initial_direction)
    return bristle


class Paintbrush:
    def __init__(self, position=[0, 0], bristles=1, shape=skimage.morphology.disk(10)):
        position = np.array(position)
        self.position = position
        self.bristles = []

        for _ in range(bristles):
            # self.bristles.append((Bristle(), random.choice(np.argwhere(np.array(shape)))))
            self.bristles.append((random_bristle(), random.choice(np.argwhere(np.array(shape)))))

    def move(self, direction):
        direction = np.array(direction)
        self.position = self.position + direction
        for bristle, bristle_pos in self.bristles:
            bristle.next(-direction)

    def draw(self):
        rr, cc = np.array([], dtype=np.int64), np.array([], dtype=np.int64)
        for bristle, bristle_pos in self.bristles:
            rr_, cc_ = bristle.draw(self.position + bristle_pos)
            rr = np.concatenate([rr, rr_])
            cc = np.concatenate([cc, cc_])
        return rr, cc


def random_paintbrush(position=[0, 0],
                      bristles_min=1, bristles_max=100,
                      shape_disk_min_radius=4, shape_disk_max_radius=15):
    bristles = random.randint(bristles_min, bristles_max)
    shape = skimage.morphology.disk(random.randint(shape_disk_min_radius,
                                                   shape_disk_max_radius))
    paintbrush = Paintbrush(position=position,
                            bristles=bristles,
                            shape=shape)
    return paintbrush


def random_brushstroke(size_x, size_y):
    X = np.zeros((size_x, size_y), dtype=np.uint64)
    # I do not know which one is the good one
    '''
    rr, cc = skimage.draw.bezier_curve(
        random.randint(round(size_x/10), round(size_x/2-size_x/10)),
        random.randint(round(size_y/10), round(size_y/2-size_y/10)),
        random.randint(round(size_x/10), round(size_x-size_x/10)),
        random.randint(round(size_y/10), round(size_y-size_y/10)),
        random.randint(round(size_x/2+size_x/10), round(size_x-size_x/10)),
        random.randint(round(size_y/2+size_y/10), round(size_y-size_y/10)),
        1)
    '''
    rr, cc = skimage.draw.bezier_curve(
        random.randint(round(size_x/2+size_x/10), round(size_x-size_x/10)),
        random.randint(round(size_y/2+size_y/10), round(size_y-size_y/10)),
        random.randint(round(size_x/10), round(size_x-size_x/10)),
        random.randint(round(size_y/10), round(size_y-size_y/10)),
        random.randint(round(size_x/10), round(size_x/2-size_x/5)),
        random.randint(round(size_y/10), round(size_y/2-size_y/5)),
        1)
    paintbrush = random_paintbrush(position=[rr[0], cc[0]],
                                   bristles_min=250, bristles_max=300,
                                   shape_disk_min_radius=25, shape_disk_max_radius=50)
    assert len(rr) == len(cc)
    for i in range(1, len(rr)-len(rr)//100):
        paintbrush.move([rr[i] - rr[i-1], cc[i] - cc[i-1]])
        Y = np.zeros((size_x, size_y), dtype=np.uint64)
        try:
            Y[paintbrush.draw()] = 1
        except Exception as e:
            print(e)
        Y = skimage.morphology.binary_dilation(Y, skimage.morphology.disk(2))
        X = X + Y

    X = np.clip(X, 0, 255).astype(np.uint8)
    X = skimage.morphology.closing(X, skimage.morphology.disk(2))

    noise = np.random.normal(0, 4, (size_x, size_y))
    X = np.where(X > 0, np.clip(X+noise, 0, 255), X).astype(np.uint8)
    return X


if __name__ == '__main__':
    X = random_brushstroke(512, 512)

    plt.imshow(X, cmap='gray', interpolation='nearest')
    plt.gca().invert_yaxis()
    plt.show()
