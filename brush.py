import random
import numpy as np
import skimage.draw
import skimage.morphology


def normalize(v):
    return v / np.sqrt(np.sum(v**2))


class Bristle:
    def __init__(self, length=100, rigidity=0.15, initial_direction=[1, 0]):
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

    def next(self, direction, w=0.15):
        direction = np.array(direction)
        p2 = normalize(w * normalize(self.p2) + (1 - w) * direction) * self.length
        p2_vector = p2 - self.p2
        self.p1 = 0.5 * self.p2 + 0.5 * self.p0
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


class Paintbrush:
    def __init__(self, position=[0, 0], bristles=1, shape=skimage.morphology.disk(1)):
        position = np.array(position)
        self.position = position
        self.bristles = []
        for _ in range(bristles):
            self.bristles.append((Bristle(), random.choice(np.argwhere(np.array(shape)))))

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
