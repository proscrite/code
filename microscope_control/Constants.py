AURTHUR = 'Nir Kapon'

FILTERS = \
    {
        1: "Center-NA_Width-NA",
        2: "Center-438nm_Width-28nm",
        3: "Center-472nm_Width-35nm",
        4: "Center-500nm_Width-29nm",
        5: "Center-527nm_Width-22nm",
        6: "Center-549nm_Width-21nm",
        7: "Center-561nm_Width-21nm",
        8: "Center-586nm_Width-26nm",
        9: "Center-605nm_Width-22nm",
        10: "Center-631nm_Width-28nm",
        11: "Center-661nm_Width-26nm",
        12: "Center-692nm_Width-47nm"
    }


FILTERS_BANDS = \
    {
        1:  (None, None),
        2:  (438, 28),
        3:  (472, 35),
        4:  (500, 29),
        5:  (527, 22),
        6:  (549, 21),
        7:  (561, 21),
        8:  (586, 26),
        9:  (605, 22),
        10: (631, 28),
        11: (661, 26),
        12: (692, 47)
    }
NUMBER_OF_FILTERS = 12
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
IMAGE_SET_SAVE_LOCATION = "data\\img\\sets\\"
IMAGE_SINGLE_SAVE_LOCATION = "data\\img\\singles\\"
NP_SAVE_LOCATION = "data\\numpy\\"
EXIFTOOL_APP = "exiftool.exe"
EXIFTOOL_OK_STRING = "1 image files updated"
# image metadata format [object_filmed, exposure, power + stretch factor] filter will be the file name
# will be inputted into [ImageDescription, XPComment, XPComment]

SAMPLES = \
    {
        0:  'other',
        1:  'RuSL',
        2:  'gold nanoparticles',
        3:  'resolution target',
        4:  'Bromobimane_Acetonitrile',
        5:  'Bromobimane_H2O',
    }

# camera prop id
DEFECT_CORRECT_MODE_ID = 0x00470010
EXPOSURE_TIME_CONTROL_ID = 0x001F0130
EXPOSURE_TIME = 0x001F0110
BURNT_PIXEL_VALUE = 100

# camera settings
DEFECT_CORRECT_MODE = 1.0       # DEFECT CORRECT MODE 1 = off, 2 = on
EXPOSURE_TIME_CONTROL = 2.0     # EXPOSURE TIME CONTROL - normal

# power meter
LASER_WAVELENGTH = 405          # nm
AVG_TIME = 10                   # s








