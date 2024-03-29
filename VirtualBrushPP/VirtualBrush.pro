QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

SOURCES += \
    main.cpp \
    virtualbrushgui.cpp \
    bezier.cpp \
    bristle.cpp \
    paintbrush.cpp

HEADERS += \
    virtualbrushgui.h \
    bezier.h \
    bristle.h \
    paintbrush.h

FORMS += \
    virtualbrushgui.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
