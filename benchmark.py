import random
import time
import bezier
import skimage.draw


def benchmark_bezier(iteration=1000000):
    a, b, c, d, e, f = [], [], [], [], [], []
    for i in range(iteration):
        a.append(random.randint(0, 100))
        b.append(random.randint(0, 100))
        c.append(random.randint(100, 400))
        d.append(random.randint(100, 400))
        e.append(random.randint(400, 500))
        f.append(random.randint(400, 500))

    print('| method | time (s) |')
    print('| ------ | -------- |')

    # warmup
    for i in range(iteration//10):
        bezier.bezier_fast(a[i], b[i],
                           c[i], d[i],
                           e[i], f[i],
                           10)
        bezier.bezier(a[i], b[i],
                           c[i], d[i],
                           e[i], f[i],
                           10)
        skimage.draw.bezier_curve(a[i], b[i],
                                  c[i], d[i],
                                  e[i], f[i],
                                  1)

    t0 = time.time()
    for i in range(iteration):
        bezier.bezier_fast(a[i], b[i],
                           c[i], d[i],
                           e[i], f[i],
                           10)
    t1 = time.time()
    print(f'| bezier.bezier_fast | {round(t1 - t0, 2)} |')


    t0 = time.time()
    for i in range(iteration):
        bezier.bezier(a[i], b[i],
                      c[i], d[i],
                      e[i], f[i],
                      10)
    t1 = time.time()
    print(f'| bezier.bezier | {round(t1 - t0, 2)} |')


    t0 = time.time()
    for i in range(iteration):
        skimage.draw.bezier_curve(a[i], b[i],
                                  c[i], d[i],
                                  e[i], f[i],
                                  1)
    t1 = time.time()
    print(f'| skimage.draw.bezier_curve | {round(t1 - t0, 2)} |')


if __name__ == '__main__':
    benchmark_bezier()
