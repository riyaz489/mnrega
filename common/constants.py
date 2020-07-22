""" this file is used to define constants, which are used in this project."""

import enum


class BackButton(enum.Enum):
    """
    This is used to provide constants for menu back buttons and exit button functionality.
    """
    BACK = 1
    EXIT = 2


class BdoFeatures(enum.Enum):
    """
    This is used to provide constants for bdo menu.
    """
    SHOW_GPM = 1
    SHOW_MEMBERS = 2
    CREATE_GPM = 3
    DELETE_GPM = 4
    UPDATE_GPM = 5
    CREATE_PROJECT = 6
    UPDATE_PROJECT = 7
    DELETE_PROJECT = 8
    SHOW_PROJECTS = 9
    SHOW_REQUESTS = 10


class GpmFeatures(enum.Enum):
    """
    This is used to provide constants for gpm menu.
    """
    SHOW_PROJECTS = 1
    PROJECT_COMPLETION = 2
    ASSIGN_MEMBERS_TO_PROJECTS = 3
    COMPLETE_MEMBER_PROJECT = 4
    CREATE_MEMBERS = 5
    SHOW_MEMBERS = 6
    UPDATE_MEMBERS = 7
    SHOW_REQUESTS = 8


class MemberFeatures(enum.Enum):
    """
    This is used to provide constants for members menu.
    """
    VIEW_DETAILS = 1
    FILE_COMPLAIN = 2


class ComplainRecipients(enum.Enum):
    """
    This is used to provide constants for complain receivers.
    """
    BDO = 1
    GPM = 2


class GpmUpdateFields(enum.Enum):
    """
    This is used to provide constants for updating gpm details.
    """
    PASSWORD = 1
    USER_NAME = 2
    NAME = 3
    STATE = 4
    DISTRICT = 5
    PINCODE = 6
    AGE = 7
    GENDER = 8


class ProjectsUpdateFields(enum.Enum):
    """This is used to provide constants for updating project details."""
    NAME = 1
    TOTAL_LABOUR_REQUIRED = 2
    ESTIMATED_COST = 3
    AREA_OF_PROJECT = 4
    ESTIMATED_START_DATE = 5
    ESTIMATED_END_DATE = 6
    PROJECT_TYPE = 7


class Role(enum.Enum):
    """This is used to provide constants for different roles in the project."""
    # Block Development Officer
    BDO = 1
    # Gram Panchayat Member
    GPM = 2
    # MGNREGA members
    Member = 3


class ProjectType(enum.Enum):
    """This is used to provide constants for different project types."""
    ROAD_CONSTRUCTION = 1
    SEWAGE_TREATMENT = 2
    BUILDING_CONSTRUCTION = 3


class RequestType(enum.Enum):
    """This is used to provide constants for different request types."""
    APPROVAL = 1
    ISSUES = 2


class RequestResult(enum.Enum):
    """This is used to provide constants for different request results."""
    APPROVED = 1
    REJECTED = 2


class ApprovalType(enum.Enum):
    """
    This is used to provide constants for different approval types.
    """
    WAGE = 1
    MEMBER = 2


class Base:
    """this class is used to define constants for console formatting."""
    # Formatting
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # End colored text
    END = '\033[0m'
    # No Color
    NC = '\x1b[0m'


class Color:
    """this class is used to define constants for console coloring."""

    # Foreground
    F_Default = "\x1b[39m"
    F_Black = "\x1b[30m"
    F_Red = "\x1b[31m"
    F_Green = "\x1b[32m"
    F_Yellow = "\x1b[33m"
    F_Blue = "\x1b[34m"
    F_Magenta = "\x1b[35m"
    F_Cyan = "\x1b[36m"
    F_LightGray = "\x1b[37m"
    F_DarkGray = "\x1b[90m"
    F_LightRed = "\x1b[91m"
    F_LightGreen = "\x1b[92m"
    F_LightYellow = "\x1b[93m"
    F_LightBlue = "\x1b[94m"
    F_LightMagenta = "\x1b[95m"
    F_LightCyan = "\x1b[96m"
    F_White = "\x1b[97m"

    # Background
    B_Default = "\x1b[49m"
    B_Black = "\x1b[40m"
    B_Red = "\x1b[41m"
    B_Green = "\x1b[42m"
    B_Yellow = "\x1b[43m"
    B_Blue = "\x1b[44m"
    B_Magenta = "\x1b[45m"
    B_Cyan = "\x1b[46m"
    B_LightGray = "\x1b[47m"
    B_DarkGray = "\x1b[100m"
    B_LightRed = "\x1b[101m"
    B_LightGreen = "\x1b[102m"
    B_LightYellow = "\x1b[103m"
    B_LightBlue = "\x1b[104m"
    B_LightMagenta = "\x1b[105m"
    B_LightCyan = "\x1b[106m"
    B_White = "\x1b[107m"
