/*
#include <iostream>
#include "bezier.h"
#include "bristle.h"

int main()
{
    std::cout << "Hello World!" << std::endl;
    Bristle *b = new Bristle();
    b->next();
    b->draw();

    std::vector<std::pair<int, int>> test = bezier(0, 0, 50, 75, 100, 100);
    for(int x = 0; x < test.size() ; ++x)
    {
        std::cout << test.at(x).first << ' ' << test.at(x).second << std::endl;
    }

    std::cout << "Bye Bye World!" << std::endl;

    return 0;
}
*/

#include "virtualbrushgui.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    VirtualBrushGUI w;
    w.show();
    return a.exec();
}
