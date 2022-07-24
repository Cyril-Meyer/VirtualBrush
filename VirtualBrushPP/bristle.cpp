#include "bristle.h"

Bristle::Bristle(float length, float rigidity, unsigned int width, glm::vec2 initial_direction)
{
    this->length = length;
    this->rigidity = rigidity;
    this->width = width;
    this->p0 = glm::vec2(0.0f, 0.0f);
    this->p2 = glm::normalize(initial_direction) * length;
    this->p1 = 0.5f * this->p1 + 0.5f * this->p2;
}

void Bristle::next(glm::vec2 direction, float weight)
{
    std::default_random_engine generator;
    std::uniform_real_distribution<float> distribution(0.0, 0.25);

    // p2 go to the direction of direction
    glm::vec2 p2 = normalize(weight * normalize(this->p2) + (1 - weight) * direction) * length;
    glm::vec2 p2_vec = p2 - this->p2;
    // p1 is between old p0 and p2 with previous p1 random 'inertia'
    float p1_noise = distribution(generator);
    glm::vec2 old_p1 = this->p1;
    this->p1 = 0.5f * this->p2 + 0.5f * this->p0;
    this->p1 = (1 - p1_noise) * this->p1 + p1_noise * old_p1;
    // set p2 position
    this->p2 = normalize(this->p2 + p2_vec * rigidity) * length;
    // p1 symmetry
    this->p1 = this->p1 + (0.5f * this->p2 + 0.5f * this->p0) -
               this->p1 + (0.5f * this->p2 + 0.5f * this->p0) -
               this->p1;
}

std::vector<std::pair<int, int>> Bristle::draw(glm::vec2 origin)
{
    return bezier(origin.x, origin.y,
                  origin.x + p1.x, origin.y + p1.y,
                  origin.x + p2.x, origin.y + p2.y
                  );
}

BristleGenerator::BristleGenerator(float length_min, float length_max, float rigidity_min, float rigidity_max, unsigned int width_min, unsigned int width_max, glm::vec2 initial_direction, float intial_direction_epsilon):
    length_min(length_min),
    length_max(length_max),
    rigidity_min(rigidity_min),
    rigidity_max(rigidity_max),
    width_min(width_min),
    width_max(width_max),
    initial_direction(initial_direction),
    intial_direction_epsilon(intial_direction_epsilon)
{
}

Bristle* BristleGenerator::get()
{
    std::uniform_real_distribution<float> d_length(length_min, length_max);
    std::uniform_real_distribution<float> d_rigidity(rigidity_min, rigidity_max);
    std::uniform_int_distribution<unsigned int> d_width(width_min, width_max);

    std::uniform_real_distribution<float> d_dir_epsilon(-intial_direction_epsilon, intial_direction_epsilon);
    glm::vec2 d_epsilon = glm::vec2(d_dir_epsilon(generator), d_dir_epsilon(generator));
    return new Bristle(d_length(generator), d_rigidity(generator), d_width(generator), initial_direction+d_epsilon);
}
