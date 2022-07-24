#include "bezier.h"

// https://github.com/SagarGaniga/computer-graphics
std::vector<std::pair<int, int>> bresenham(int x0, int y0, int x1, int y1)
{
    std::vector<std::pair<int, int>> pixels;
    float dx = (float)x1 - (float)x0;
    float dy = (float)y1 - (float)y0;

    float xsign = (dx > 0.0f) ? 1.0f : (-1.0f);
    float ysign = (dy > 0.0f) ? 1.0f : (-1.0f);

    dx = std::abs(dx);
    dy = std::abs(dy);

    float xx, xy, yx, yy = 0.0f;

    if(dx > dy)
    {
        xx = xsign;
        yy = ysign;
    }
    else
    {
        xy = ysign;
        yx = xsign;
    }

    float d = 2*dy - dx;
    float y = 0.0f;

    std::pair<int, int> p;

    for(int x = 0; x <= dx; ++x)
    {
        p = std::make_pair((int)std::round((float)x0 + (float)x*xx + (float)y*yx),
                           (int)std::round((float)y0 + (float)x*xy + (float)y*yy));

        if(d >= 0)
        {
            y += 1;
            d -= 2*dx;
        }
        d += 2*dy;

        pixels.push_back(p);
    }

    return pixels;
}

std::vector<std::pair<int, int> > bezier(int x0, int y0, int x1, int y1, int x2, int y2, unsigned int n_samples)
{
    std::vector<std::pair<int, int>> pixels;
    pixels.push_back(std::make_pair(x0, y0));

    int x_old = x0;
    int y_old = y0;
    float t;
    int x, y;
    std::vector<std::pair<int, int>> bresenham_pixels;

    for(unsigned int t_ = 0; t_ <= n_samples; ++t_)
    {
        t = (float)t_/(float)n_samples;
        x = (int)std::round((1-t)*((1-t)*x0 + t*x1) + t*((1-t)*x1 + t*x2));
        y = (int)std::round((1-t)*((1-t)*y0 + t*y1) + t*((1-t)*y1 + t*y2));
        bresenham_pixels = bresenham(x_old, y_old, x, y);
        pixels.insert(pixels.end(), bresenham_pixels.begin(), bresenham_pixels.end());
        x_old = x;
        y_old = y;
    }

    return pixels;
}
