#ifndef PAINTBRUSH_H
#define PAINTBRUSH_H

#include <random>
#include "glm/glm.hpp"
#include "bristle.h"

class Paintbrush
{
public:
    Paintbrush(glm::vec2 position, unsigned int bristles, BristleGenerator bristle_generator, std::vector<std::pair<int, int>> shape);
    void move(glm::vec2 direction, float weight=0.05f);
    std::vector<std::pair<int, int>> draw();


private:
    glm::vec2 position;
    std::vector<std::pair<Bristle*, std::pair<int, int>>> bristles;
};


class PaintbrushGenerator
{
public:
    PaintbrushGenerator(std::vector<std::pair<int, int>> shape, glm::vec2 position=glm::vec2(0.0f, 0.0f), unsigned int bristles_min=10, unsigned int bristles_max=50, BristleGenerator bristle_generator=BristleGenerator());

    Paintbrush* get();

private:
    glm::vec2 position;
};

#endif // PAINTBRUSH_H
