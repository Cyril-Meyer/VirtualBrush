#ifndef BEZIER_H
#define BEZIER_H

#include <cmath>
#include <vector>

std::vector<std::pair<int, int>> bresenham(int x0, int y0, int x1, int y1);
std::vector<std::pair<int, int>> bezier(int x0, int y0, int x1, int y1, int x2, int y2, unsigned int n_samples=10);

#endif // BEZIER_H
