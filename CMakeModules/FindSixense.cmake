# This script locates the Sixense SDK
# ------------------------------------
#
# usage:
# find_package(Sixense ...)
#
# searches in SIXENSE_ROOT and usual locations
#
# Sets SIXENSE_INCLUDE_DIR, SIXENSE_LIBRARY_STATIC and SIXENSE_LIBRARY_DYNAMIC

set(SIXENSE_POSSIBLE_PATHS
	${SIXENSE_ROOT}
	$ENV{SIXENSE_ROOT}
	"C:/Program Files/Steam/steamapps/common/sixense sdk/SixenseSDK"
	"C:/Program Files (x86)/Steam/steamapps/common/sixense sdk/SixenseSDK"
	~/Library/Frameworks
	/Library/Frameworks
	/usr/local/
	/usr/
	/sw # Fink
	/opt/local/ # DarwinPorts
	/opt/csw/ # Blastwave
	/opt/
	)


find_path(SIXENSE_INCLUDE_DIR sixense.h
	PATH_SUFFIXES
		"include"
	PATHS
		${SIXENSE_POSSIBLE_PATHS}
	)

find_library(SIXENSE_LIBRARY_STATIC sixense_s
	PATH_SUFFIXES
		"lib"
		"lib/win32/release_static"
	PATHS
		${SIXENSE_POSSIBLE_PATHS}
	)

find_library(SIXENSE_LIBRARY_DYNAMIC sixense
	PATH_SUFFIXES
		"lib"
		"lib/win32/release_dll"
		"lib/linux/release"
	PATHS
		${SIXENSE_POSSIBLE_PATHS}
	)

if ((NOT SIXENSE_INCLUDE_DIR) OR ((NOT SIXENSE_LIBRARY_STATIC) AND (NOT SIXENSE_LIBRARY_DYNAMIC)))
    if(Sixense_FIND_REQUIRED) #prefix is filename, case matters
        message(FATAL_ERROR "Could not find Sixense SDK!")
    elseif(NOT Sixense_FIND_QUIETLY)
        message("Could not find Sixense SDK!")
    endif(Sixense_FIND_REQUIRED)
endif ((NOT SIXENSE_INCLUDE_DIR) OR ((NOT SIXENSE_LIBRARY_STATIC) AND (NOT SIXENSE_LIBRARY_DYNAMIC)))

if (NOT Sixense_FIND_QUIETLY)
	message("Found Sixense SDK: ${SIXENSE_INCLUDE_DIR}")
endif (NOT Sixense_FIND_QUIETLY)
