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

void VirtualBrushGUI::on_actionBristle_triggered()
{
    QImage *image = new QImage(512, 512, QImage::Format_RGB888);
    image->fill(QColor(0, 0, 0));
    QColor color = QColor(0, 0, 255);

    Bristle *b = new Bristle();
    std::vector<std::pair<int, int>> pixels = b->draw();
    std::pair<int, int> pixel;

    for(std::size_t i = 0; i < pixels.size(); ++i)
    {
        pixel = pixels.at(i);
        image->setPixelColor(pixel.first, pixel.second, color);
    }

    for(int i = 0; i < 10; ++i)
    {
        b->next(glm::vec2(1.0, 1.0));
        pixels = b->draw();
        for(std::size_t i = 0; i < pixels.size(); ++i)
        {
            pixel = pixels.at(i);
            image->setPixelColor(pixel.first, pixel.second, color);
        }
    }

    ui->label->setPixmap(QPixmap::fromImage(*image, Qt::AutoColor));
}
