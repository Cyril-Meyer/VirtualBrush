#ifndef VIRTUALBRUSHGUI_H
#define VIRTUALBRUSHGUI_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class VirtualBrushGUI; }
QT_END_NAMESPACE

class VirtualBrushGUI : public QMainWindow
{
    Q_OBJECT

public:
    VirtualBrushGUI(QWidget *parent = nullptr);
    ~VirtualBrushGUI();

private:
    Ui::VirtualBrushGUI *ui;
};
#endif // VIRTUALBRUSHGUI_H
