#include "virtualbrushgui.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    VirtualBrushGUI w;
    w.show();
    return a.exec();
}
