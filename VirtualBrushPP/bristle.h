#ifndef BRISTLE_H
#define BRISTLE_H

#include <random>
#include "glm/glm.hpp"
#include "bezier.h"

class Bristle
{
public:
    Bristle(float length=100.0f, float rigidity=0.1f, unsigned int width=1, glm::vec2 initial_direction=glm::vec2(1.0, 1.0));
    void next(glm::vec2 direction=glm::vec2(1.0f, 1.0f), float weight=0.05f);
    std::vector<std::pair<int, int>> draw(glm::vec2 origin=glm::vec2(0.0f, 0.0f));

private:
    float length;
    float rigidity;
    unsigned int width;
    glm::vec2 p0;
    glm::vec2 p1;
    glm::vec2 p2;
};

class BristleGenerator
{
public:
    BristleGenerator(float length_min=1.0f, float length_max = 100.0f,
                     float rigidity_min=0.05f, float rigidity_max=0.15f,
                     unsigned int width_min=1, unsigned int width_max=1,
                     glm::vec2 initial_direction=glm::vec2(1.0, 1.0), float intial_direction_epsilon=1.0f);

    Bristle* get();

private:
    std::default_random_engine generator;
    float length_min;
    float length_max;
    float rigidity_min;
    float rigidity_max;
    unsigned int width_min;
    unsigned int width_max;
    glm::vec2 initial_direction;
    float intial_direction_epsilon;
};

#endif // BRISTLE_H
