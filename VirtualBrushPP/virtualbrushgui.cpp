#include "virtualbrushgui.h"
#include "ui_virtualbrushgui.h"

VirtualBrushGUI::VirtualBrushGUI(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::VirtualBrushGUI)
{
    ui->setupUi(this);
}

VirtualBrushGUI::~VirtualBrushGUI()
{
    delete ui;
}

