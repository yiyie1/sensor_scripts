import ctypes as c
import time
import argparse

FPC_SUCCESS = 0
SWING_SPI_FREQUENCY_HZ = 5000000

class GpioCtrl(c.Structure):
    __field__= [
        ("led_override", c.c_bool),
        ("directions", c.c_int * 3),
        ("levels", c.c_int * 3)
    ]

class FpcHalDeviceHandle_t(c.Structure):
    __fields__ = [
        ("comm_handle", c.c_void_p),
        ("device_type", c.c_int),
        ("log_callback", c.c_void_p),
        ("gpio_ctrl", GpioCtrl),
        ("hal_func", c.c_void_p),
        ("hal_func_handle", c.c_void_p)
    ]

class HAL(object):
    def __init__(self, hal_library_name):
        self.hal_library_name = hal_library_name
        self.hal_dll = c.CDLL(hal_library_name)
        assert self.hal_dll != None

    def setup_interface(self):
        self.OpenDevice = self.hal_dll.HalOpenDevice
        self.SetResetLow = self.hal_dll.HalSetResetLow
        self.WriteReadSpi = self.hal_dll.HalWriteReadSpi
        self.ReadIrq = self.hal_dll.HalReadIrq
        self.SetResetHigh = self.hal_dll.HalSetResetHigh
        self.SetLedIndicators = self.hal_dll.HalSetLedIndicators
        self.SetSpiFrequency = self.hal_dll.HalSetSpiFrequency
        self.CloseDevice = self.hal_dll.HalCloseDevice

    def __str__(self):
        return self.hal_library_name + ": " + str(self.hal_dll)

def SetUpDevice(MyHal, device):
    str_format = None
    status = MyHal.OpenDevice(c.pointer(device), str_format)
    if status != FPC_SUCCESS:
        print("OpenDevice fail:", status)
        return status

    status = MyHal.SetSpiFrequency(c.pointer(device), SWING_SPI_FREQUENCY_HZ)
    if status != FPC_SUCCESS:
        print("OpenDevice fail:", status)
        return status

    status = MyHal.SetResetLow(c.pointer(device))
    if status != FPC_SUCCESS:
        print("SetResetLow fail:", status)
        return status

    time.sleep(0.1)

    status = MyHal.SetResetHigh(c.pointer(device))
    if status != FPC_SUCCESS:
        print("SetResetHigh fail:", status)
        return status

    status = MyHal.SetLedIndicators(c.pointer(device), True, True, True)
    if status != FPC_SUCCESS:
        print("SetResetHigh fail:", status)
        return status

    time.sleep(0.1)

    status = MyHal.SetLedIndicators(c.pointer(device), False, False, False)
    if status != FPC_SUCCESS:
        print("SetResetHigh fail:", status)
        return status

    irq = c.create_string_buffer(1)

    status = MyHal.ReadIrq(c.pointer(device), irq)
    if status != FPC_SUCCESS:
        print("SetResetHigh fail:", status)
        return status

    if irq.raw == b'\x01':
        return FPC_SUCCESS
    else:
        print("Incorrect IRQ", irq.raw)
        return -1

def RunSPI(cmd, data, device):
    values = data.split(",")

    if cmd == "read":
        value = int(values[0], 16) if values[0].startswith('0x') else int(values[0])
        read_buffer_len = int(values[-1])
        read_buffer = c.create_string_buffer(read_buffer_len)
        cmd = c.c_char(value)

        status = MyHal.WriteReadSpi(c.pointer(device), c.byref(cmd), 1, read_buffer, read_buffer_len)
        if status != FPC_SUCCESS:
            print("Read SPI fail:", status)
        else:
            print("Read SPI success, buffer:", read_buffer.raw)

    elif cmd == "write":
        write_buffer_len = len(values)
        cmd = (c.c_char * write_buffer_len)()
        for i, val in enumerate(values):
            cmd[i] = int(val, 16) if val.startswith('0x') else int(val)

        status = MyHal.WriteReadSpi(c.pointer(device), c.byref(cmd), write_buffer_len, None, 0)

        if status != FPC_SUCCESS:
            print("Write SPI fail:", status)
        else:
            print("Write SPI success")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', help = "Read SPI", type=str)
    parser.add_argument('-w', help="Write SPI", type=str)

    args = parser.parse_args()

    if args.r is None and args.w is None:
        print("Please pass -r or -w")

    else:
        MyHal = HAL(r"hal_ftdi.dll")
        MyHal.setup_interface()

        device = FpcHalDeviceHandle_t()

        try:
            status = SetUpDevice(MyHal, device)

            if status == FPC_SUCCESS:
                if args.w:
                    for val in args.w.split(";"):
                        RunSPI("write", val, device)
                if args.r:
                    for val in args.r.split(";"):
                        RunSPI("read", val, device)
        finally:
            MyHal.CloseDevice(c.pointer(device))

