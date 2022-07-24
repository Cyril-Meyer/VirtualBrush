#include "bezier.h"
#include "bristle.h"
#include "paintbrush.h"

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
namespace py = pybind11;


void brushstroke(py::array_t<uint8_t> result)
{
    // std::vector<std::pair<int, int>> brushstroke(std::vector<std::pair<int, int>> path, Paintbrush paintbrush);
	return;
}

PYBIND11_MODULE(VirtualBrushPP, m) {
    m.def("brushstroke", &brushstroke, "Fill array with a random brushstroke");
}

