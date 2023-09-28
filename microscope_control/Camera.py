import dcam
from Constants import *
import numpy as np


class Camera:
    def __init__(self):
        self.camera = False
        self.time_out = 1000
        self.exposure = 0.5

    def __del__(self):
        if self:
            self.close()

    def __bool__(self):
        if self.camera is False:
            return False
        return True

    def open(self, iDevice=0):
        if self:
            # print('camera already open')
            return True
        if dcam.Dcamapi.init() is not False:
            camera = dcam.Dcam(iDevice)
            if camera.dev_open() is not False:
                if camera.buf_alloc(1) is not False:
                    camera.prop_setvalue(DEFECT_CORRECT_MODE_ID,
                                         DEFECT_CORRECT_MODE)  # DEFECT CORRECT MODE 1 = off, 2 = on
                    camera.prop_setvalue(EXPOSURE_TIME_CONTROL_ID,
                                         EXPOSURE_TIME_CONTROL)  # EXPOSURE TIME CONTROL - normal
                    self.camera = camera
                    return True
                else:
                    print('-NG: Dcam.buf_alloc(1) fails with error {}'.format(camera.lasterr()))
                camera.dev_close()
            else:
                print('-NG: Dcam.dev_open() fails with error {}'.format(camera.lasterr()))
        else:
            print('-NG: Dcamapi.init() fails with error {}'.format(dcam.Dcamapi.lasterr()))
        print('error connecting to camera')
        return False

    def close(self):
        if self:
            self.camera.buf_release()
            self.camera.dev_close()
            dcam.Dcamapi.uninit()
            self.camera = False

    def exposure_time(self, exposure):
        if self is False:
            print('no active camera')
            return False
        self.exposure = exposure
        self.camera.prop_setvalue(EXPOSURE_TIME, exposure)  # EXPOSURE TIME
        self.time_out = np.max((int(exposure * 2 * 1000), int(MIN_TIME_OUT * 1000)))
        return self.camera.prop_getvalue(EXPOSURE_TIME)

    def take_picture(self):
        if self is False:
            print('no active camera')
            return False
        if self.camera.cap_snapshot() is not False:
            if self.camera.wait_capevent_frameready(self.time_out) is not False:
                data = self.camera.buf_getlastframedata()
                data[1466][110] = BURNT_PIXEL_VALUE
                data[1049][214] = BURNT_PIXEL_VALUE
                data[686][432] = BURNT_PIXEL_VALUE
                data[1365][2009] = BURNT_PIXEL_VALUE
                data[1301][656] = BURNT_PIXEL_VALUE
                data[137][1824] = BURNT_PIXEL_VALUE
                data[1643][2] = BURNT_PIXEL_VALUE
                data[1669][357] = BURNT_PIXEL_VALUE
                data[1455][1761] = BURNT_PIXEL_VALUE
                data[986][180] = BURNT_PIXEL_VALUE
                data[458][220] = BURNT_PIXEL_VALUE
                data[1243][1006] = BURNT_PIXEL_VALUE
                data[1467][632] = BURNT_PIXEL_VALUE
                data[794][912] = BURNT_PIXEL_VALUE
                data[1634][1347] = BURNT_PIXEL_VALUE
                return data
        print("Failed taking a snapshot")  # improve
        camera_error = self.camera.lasterr()
        print('-NG: camera.wait_event() fails with error {}'.format(camera_error))
        return False

    def show_prop_camera(self):
        if self.camera is False:
            print('Failed connecting to camera')
            return
        idprop = self.camera.prop_getnextid(0)
        while idprop is not False:
            output = '0x{:08X}: '.format(idprop)

            propname = self.camera.prop_getname(idprop)
            if propname is not False:
                output = output + propname + "\t" + str(self.camera.prop_getvalue(idprop))
            print(output)
            idprop = self.camera.prop_getnextid(idprop)




