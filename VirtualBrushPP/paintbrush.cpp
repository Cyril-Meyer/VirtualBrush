#include "paintbrush.h"

Paintbrush::Paintbrush(glm::vec2 position, unsigned int bristles, BristleGenerator bristle_generator, std::vector<std::pair<int, int> > shape)
{
    this->position = position;

    std::default_random_engine generator;
    std::uniform_int_distribution<int> distribution(0,shape.size());
    std::pair<Bristle*, std::pair<int, int>> bristle;

    for(unsigned int i = 0; i < bristles; ++i)
    {
        bristle = std::make_pair(bristle_generator.get(), shape.at(distribution(generator)));

        this->bristles.push_back(bristle);
    }
}

void Paintbrush::move(glm::vec2 direction, float weight)
{
    this->position += direction;
    for(std::size_t i = 0; i < bristles.size() ; ++i)
    {
        bristles.at(i).first->next(-direction, weight);
    }
}

std::vector<std::pair<int, int> > Paintbrush::draw()
{
    std::vector<std::pair<int, int> > pixels;
    std::vector<std::pair<int, int> > tmp;
    for(std::size_t i = 0; i < bristles.size() ; ++i)
    {
        glm::vec2 origin = glm::vec2(bristles.at(i).second.first, bristles.at(i).second.second);
        tmp = bristles.at(i).first->draw();
        pixels.insert(pixels.end(), tmp.begin(), tmp.end());
    }
    return pixels;
}
