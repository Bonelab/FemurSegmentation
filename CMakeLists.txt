cmake_minimum_required(VERSION 2.8)
SET(CMAKE_CXX_STANDARD 14)

project(FemurSegmentation)

# ITK
find_package(ITK REQUIRED)
include(${ITK_USE_FILE})

if( "${ITK_VERSION_MAJOR}" LESS 5 )
  MESSAGE(FATAL_ERROR "You must build FemurSegmentation with ITK >= 4=5.0!")
endif( "${ITK_VERSION_MAJOR}" LESS 5 )

# Grid Cut
set(GridCutDir ${CMAKE_CURRENT_SOURCE_DIR}/lib/gridcut/include/GridCut)
set(GridCutAlphaDir ${CMAKE_CURRENT_SOURCE_DIR}/lib/gridcut/examples/include/AlphaExpansion)
set(GridCutInclude ${GridCutDir} ${GridCutAlphaDir})

# Our files
set(IncludeDir ${CMAKE_CURRENT_SOURCE_DIR}/include)

include_directories(${GridCutInclude})
include_directories(${IncludeDir})

# Add src
add_subdirectory(src)

