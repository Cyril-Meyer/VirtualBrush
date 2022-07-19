import numpy as np
import cv2
import brush

WNAME = 'VirtualBrush - brush gui'


def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # mouse_event.paintbrush = brush.Paintbrush(position=[y, x])
        mouse_event.paintbrush = brush.random_paintbrush(position=[y, x])

    if event == cv2.EVENT_MOUSEMOVE:
        if mouse_event.paintbrush is None:
            return
        DATA.fill(0)
        mouse_event.paintbrush.move([y - mouse_event.old_y, x - mouse_event.old_x])
        rr, cc = mouse_event.paintbrush.draw()
        rr = np.clip(rr, 0, DATA.shape[0]-1)
        cc = np.clip(cc, 0, DATA.shape[1]-1)
        DATA[rr, cc, 0] = 255

    mouse_event.old_x = x
    mouse_event.old_y = y


mouse_event.paintbrush = None
mouse_event.old_x = None
mouse_event.old_y = None


cv2.namedWindow(WNAME, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(WNAME, mouse_event)

DATA = np.zeros((512, 512, 3), dtype=np.uint8)
while True:
    cv2.imshow(WNAME, DATA)
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
