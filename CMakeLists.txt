cmake_minimum_required(VERSION 2.6)

# add cmake_modules to module search path, for find_package()
# I force CMAKE_ROOT/Modules into the module search path because it's missing in my cmake at uni - maybe that's a local problem though?
#set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMakeModules" ${CMAKE_MODULE_PATH} "${CMAKE_ROOT}/Modules")
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMakeModules" ${CMAKE_MODULE_PATH})

project("Hydra FPS")


# add OpenGL
find_package(OpenGL)
if(NOT OPENGL_FOUND)
	message(FATAL_ERROR "OpenGL not found!")
endif(NOT OPENGL_FOUND)
if(NOT OPENGL_GLU_FOUND)
	message(FATAL_ERROR "GLU not found!")
endif(NOT OPENGL_GLU_FOUND)

if(${OPENGL_INCLUDE_DIR}) # empty include dir probably means its in the compiler include dir or something.
	include_directories("${OPENGL_INCLUDE_DIR}")
endif(${OPENGL_INCLUDE_DIR})
set(LIBRARIES
	${OPENGL_gl_LIBRARY}
	${OPENGL_glu_LIBRARY}
	)

# add Bullet
if (NOT BULLET_ROOT)
	set(BULLET_ROOT $ENV{BULLET_ROOT})
endif (NOT BULLET_ROOT)
find_package(Bullet)
if(NOT BULLET_FOUND)
	message(FATAL_ERROR "Could not find Bullet Physics - try setting BULLET_ROOT")
endif(NOT BULLET_FOUND)
set(LIBRARIES
	${LIBRARIES}
	${BULLET_DYNAMICS_LIBRARY}
	${BULLET_COLLISION_LIBRARY}
	)

# add SFML
find_package(SFML 2 REQUIRED system window graphics audio)
include_directories("${SFML_INCLUDE_DIR}")
add_definitions(-DSFML_DYNAMIC) # this may be outdated? there's SFML_STATIC, this may be assumed otherwise...
if(${CMAKE_BUILD_TYPE} MATCHES Debug)
	# add debug libs
	set(LIBRARIES
		${LIBRARIES}
		${SFML_GRAPHICS_LIBRARY_DEBUG}
		${SFML_WINDOW_LIBRARY_DEBUG}
		${SFML_SYSTEM_LIBRARY_DEBUG}
		)
else(${CMAKE_BUILD_TYPE} MATCHES Debug)
	# add release libs
	set(LIBRARIES
		${LIBRARIES}
		${SFML_GRAPHICS_LIBRARY_RELEASE}
		${SFML_WINDOW_LIBRARY_RELEASE}
		${SFML_SYSTEM_LIBRARY_RELEASE}
		)
endif(${CMAKE_BUILD_TYPE} MATCHES Debug)

include_directories("include")
set(SRC_FILES
	"src/main.cpp"
	)
set(INCLUDE_FILES
	)
set(ALL_FILES ${SRC_FILES} ${INCLUDE_FILES})

add_executable("HydraFPS" ${ALL_FILES})
target_link_libraries("HydraFPS" ${LIBRARIES})