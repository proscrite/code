AURTHUR = 'Nir Kapon'

# FILTERS = \
#     {
#         1: "Center-NA_Width-NA",
#         2: "Center-438nm_Width-28nm",
#         3: "Center-472nm_Width-35nm",
#         4: "Center-500nm_Width-29nm",
#         5: "Center-527nm_Width-22nm",
#         6: "Center-549nm_Width-21nm",
#         7: "Center-561nm_Width-21nm",
#         8: "Center-586nm_Width-26nm",
#         9: "Center-605nm_Width-22nm",
#         10: "Center-631nm_Width-28nm",
#         11: "Center-661nm_Width-26nm",
#         12: "Center-692nm_Width-47nm"
#     }

FILTERS = \
    {
        1: "Center-NA_Width-NA",
        2: "Dark_Blind",
        3: "Center-438nm_Width-28nm",
        4: "Center-472nm_Width-35nm",
        5: "Center-549nm_Width-21nm",
        6: "Center-575nm_Width-35nm",
        7: "Center-586nm_Width-26nm",
        8: "Center-605nm_Width-22nm",
        9: "Center-631nm_Width-28nm",
        10: "Center-661nm_Width-26nm",
        11: "Center-676nm_Width-29nm",
        12: "Center-692nm_Width-47nm"
    }
EXCITATION_FILTER = "Center-527nm_Width-22nm",
DOUBLE_FILTER = "Center-561nm_Width-21nm"
LEFTOVER_FILTER = "Center-500nm_Width-29nm",
LASER_WAVELENGTH = "515nm"
LASER_SOURCE = {1: "TOptica",
                2: "Diode"}

DICHROIC_MIRROR_CUTTOFF = "550nm"
MICROSCOPE_OBJECTIVE = {1: "Mitutoyo_50x_NA_0.5",
                        2: "Nikon_60x_NA_0.95"}
EXPOSURE_TIME = 10

FILTERS_BANDS = \
    {
        1:  (None, None),
        2:  (None, None),
        3:  (438, 28),
        4:  (472, 35),
        5:  (549, 21),
        6:  (575, 35),
        7:  (586, 26),
        8:  (605, 22),
        9:  (631, 28),
        10: (661, 26),
        11: (676, 29),
        12: (692, 47)
    }
NUMBER_OF_FILTERS = 12
RANGE_FILTERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
STANDARD_EXPOSER = 0.075  # 0.7 lowered for measurements of Bromobimane

FILTERS_EXPOSER = \
    {
        1: 0.001,
        2: STANDARD_EXPOSER,
        3: STANDARD_EXPOSER,
        4: STANDARD_EXPOSER,
        5: STANDARD_EXPOSER,
        6: STANDARD_EXPOSER,
        7: STANDARD_EXPOSER,
        8: STANDARD_EXPOSER,
        9: STANDARD_EXPOSER,
        10: STANDARD_EXPOSER,
        11: STANDARD_EXPOSER,
        12: STANDARD_EXPOSER
    }

Starting_position = 1
MIN_TIME_OUT = 0.6              # seconds
TIME_FORMAT = "%d-%m-%y_%H-%M-%S"
TIME_FORMAT_TODAY = '%d-%m-%y'
IMAGE_SET_SAVE_LOCATION = "G:\\My Drive\\Ba Tagging\\data\\img\\sets\\"
IMAGE_SINGLE_SAVE_LOCATION = "G:\\My Drive\\Ba Tagging\\data\\img\\sing\\"
IMAGE_TIMERUN_SAVE_LOCATION = "G:\\My Drive\\Ba Tagging\\data\\img\\time\\"

NP_SAVE_LOCATION = "G:\\My Drive\\Ba Tagging\\data\\numpy\\"
EXIFTOOL_APP = "G:\\My Drive\\Ba Tagging\\code\\microscope_control\\exiftool.exe"
EXIFTOOL_OK_STRING = "1 image files updated"
# image metadata format [object_filmed, exposure, power + stretch factor] filter will be the file name
# will be inputted into [ImageDescription, XPComment, XPComment]

SAMPLES = \
    {
        0:  'other',
        'q': 'quit',
        1:  'RuSL',
        2:  'quartz',
        3:  'resolution target',
        4:  'Bromobimane_Acetonitrile',
        5:  'Bromobimane_H2O',
        6:  'FS6_Bromob_1e-6',
        7:  'IPG-4 1 µM',
        8:  'Rhodamine-B 50 µM'
    }

# camera prop id
DEFECT_CORRECT_MODE_ID = 0x00470010
EXPOSURE_TIME_CONTROL_ID = 0x001F0130
# EXPOSURE_TIME = 0x001F0110 
BURNT_PIXEL_VALUE = 100

# camera settings
DEFECT_CORRECT_MODE = 1.0       # DEFECT CORRECT MODE 1 = off, 2 = on
EXPOSURE_TIME_CONTROL = 2.0     # EXPOSURE TIME CONTROL - normal

# power meter
LASER_WAVELENGTH = 515          # nm
AVG_TIME = 2                   # s


#### TOptica power 2.1 microW





