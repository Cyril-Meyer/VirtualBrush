#ifndef VIRTUALBRUSHGUI_H
#define VIRTUALBRUSHGUI_H

#include <QMainWindow>
#include <QImage>
#include <QPixmap>

#include "bezier.h"
#include "bristle.h"
#include "paintbrush.h"

QT_BEGIN_NAMESPACE
namespace Ui { class VirtualBrushGUI; }
QT_END_NAMESPACE

class VirtualBrushGUI : public QMainWindow
{
    Q_OBJECT

public:
    VirtualBrushGUI(QWidget *parent = nullptr);
    ~VirtualBrushGUI();

private slots:
    void on_actionBristle_triggered();

private:
    Ui::VirtualBrushGUI *ui;
};
#endif // VIRTUALBRUSHGUI_H
