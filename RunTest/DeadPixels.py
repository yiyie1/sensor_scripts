from enum import IntEnum
import ctypes as c

MAX_NBR_SUB_AREA_ROWS = 4
MAX_NBR_SUB_AREA_COLS = 4

MAX_NBR_ROWS = 256
MAX_NBR_COLS = 256


product_map = {
    "1080" : 0,
    "1020" : 1,
    "1021" : 2,
    "1025" : 3,
    "1225" : 4,
    "1022" : 5,
    "1035" : 6,
    "1235" : 7,
    "1140" : 8,
    "1145" : 9,
    "1245" : 10,
    "1150" : 11,
    "1155" : 12,
    "1265" : 14,
    "1268" : 15,
    "1028" : 16,
    "1075" : 17,
    "1320" : 18,
    "1321" : 19,
    "1263" : 20,
    "1262" : 21,
    "1266" : 22,
    "1264" : 23,
    "1272" : 24,
    "1228" : 25,
    "1181" : 26,
    "1267" : 27,
    "1282" : 28,
    "1283" : 29,
    "1286" : 30}

class TestLib(object):
    def __init__(self, hal_library_name):
        self.hal_library_name = hal_library_name
        self.hal_dll = c.CDLL(hal_library_name)
        assert self.hal_dll != None

    def setup_interface(self):
        self.init_gradient_checkerboard_test_based_on_testlevel = self.hal_dll.init_gradient_checkerboard_test_based_on_testlevel
        self.gradient_checkerboard_test = self.hal_dll.gradient_checkerboard_test
        self.checkerboard_test = self.hal_dll.checkerboard_test
        self.init_checkerboard_test = self.hal_dll.init_checkerboard_test

    def __str__(self):
        return self.hal_library_name + ": " + str(self.hal_dll)

class fpc_checkerboard_config_t(c.Structure):
    _fields_ = [
        ("area_height", c.c_uint32),
        ("area_width", c.c_uint32),
        ("pixel_count", c.c_uint32),
        ("sub_area_height", c.c_uint32),
        ("sub_area_width", c.c_uint32),
        ("sub_area_nbr_rows", c.c_uint32),
        ("sub_area_nbr_cols", c.c_uint32),
        ("sub_areas_row", c.c_uint8 * MAX_NBR_SUB_AREA_ROWS),
        ("sub_areas_col", c.c_uint8 * MAX_NBR_SUB_AREA_COLS),
        ("max_deviation", c.c_uint32),
        ("pixel_errors_upper_limit", c.c_uint32),
        ("sub_areas_errors_upper_limit", c.c_uint32),
        ("CB_type1_median_min", c.c_uint32),
        ("CB_type1_median_max", c.c_uint32),
        ("CB_type2_median_min", c.c_uint32),
        ("CB_type2_median_max", c.c_uint32),
        ("ICB_type1_median_min", c.c_uint32),
        ("ICB_type1_median_max", c.c_uint32),
        ("ICB_type2_median_min", c.c_uint32),
        ("ICB_type2_median_max", c.c_uint32),
    ]

class fpc_gradient_checkerboard_config_t(c.Structure):
    _fields_ = [
        ("area_height", c.c_uint32),
        ("area_width", c.c_uint32),
        ("pixel_count", c.c_uint32),
        ("sub_area_height", c.c_uint32),
        ("sub_area_width", c.c_uint32),
        ("sub_area_nbr_rows", c.c_uint32),
        ("sub_area_nbr_cols", c.c_uint32),
        ("sub_areas_row", c.c_uint8 * MAX_NBR_SUB_AREA_ROWS),
        ("sub_areas_col", c.c_uint8 * MAX_NBR_SUB_AREA_COLS),
        ("max_deviation", c.c_uint32),
        ("pixel_errors_upper_limit", c.c_uint32),
        ("sub_areas_errors_upper_limit", c.c_uint32),
        ("histogram_slot_length", c.c_uint32),
        ("CB_type1_median_min", c.c_uint32),
        ("CB_type1_median_max", c.c_uint32),
        ("CB_type2_median_min", c.c_uint32),
        ("CB_type2_median_max", c.c_uint32),
        ("ICB_type1_median_min", c.c_uint32),
        ("ICB_type1_median_max", c.c_uint32),
        ("ICB_type2_median_min", c.c_uint32),
        ("ICB_type2_median_max", c.c_uint32),
        ("histogram_deviation", c.c_uint8)
    ]

class fpc_checkerboard_result_t(c.Structure):
    _fields_ = [
        ("pixel_errors", c.c_uint32),
        ("sub_area_errors", c.c_uint32),
        ("type1_median", c.c_uint32),
        ("type2_median", c.c_uint32),
        ("type1_mean", c.c_uint32),
        ("type2_mean", c.c_uint32),
        ("type1_deviation_max", c.c_uint32),
        ("type2_deviation_max", c.c_uint32),
        ("result", c.c_uint32),
        ("pass", c.c_bool),
        ("pixel_errors_per_row", c.c_uint8 * MAX_NBR_ROWS),
        ("pixel_errors_per_col", c.c_uint8 * MAX_NBR_COLS)
    ]

class fpc_gradient_checkerboard_result_t(c.Structure):
    _fields_ = [
        ("pixel_errors", c.c_uint32),
        ("sub_area_errors", c.c_uint32),
        ("type1_deviation_max", c.c_uint32),
        ("type2_deviation_max", c.c_uint32),
        ("type1_min_histogram_median", c.c_uint8),
        ("type2_min_histogram_median", c.c_uint8),
        ("type1_max_histogram_median", c.c_uint8),
        ("type2_max_histogram_median", c.c_uint8),
        ("result", c.c_uint32),
        ("pass", c.c_bool)
    ]

class dead_pixels_info_t(c.Structure):
    _fields_ = [
        ("num_dead_pixels", c.c_uint16),
        ("dead_pixels_index_list", c.POINTER(c.c_uint16)),
        ("list_max_size", c.c_uint16),
        ("is_initialized", c.c_int32),
    ]

class fpc_checkerboard_t(IntEnum):
    """Equivalent to prodtestlib.dll's fpc_test_level_t"""
    FPC_IMAGE_TEST_CHESS = 3,
    FPC_IMAGE_TEST_CHESS_INV = 4,
    FPC_IMAGE_TEST_WHITE = 5,
    FPC_IMAGE_TEST_BLACK = 6,


class TestLevelT(IntEnum):
    """Equivalent to prodtestlib.dll's fpc_test_level_t"""
    FPC_TEST_LEVEL_MTS = 0
    FPC_TEST_LEVEL_ITS = 1