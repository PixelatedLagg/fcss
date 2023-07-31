CMAKE_MINIMUM_REQUIRED(VERSION 3.7 FATAL_ERROR)

project("fcssProcessor"
        VERSION
            "0.0.1"
        DESCRIPTION
            "Processor for working with the fcss language"
)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# compiler must be 17
set(CMAKE_CXX_STANDARD 17)

# required if linking to static library
add_definitions(-DANTLR4CPP_STATIC)

# using /MD flag for antlr4_runtime (for Visual C++ compilers only)
set(ANTLR4_WITH_STATIC_CRT OFF)

# add external build for antlrcpp
include(ExternalAntlr4Cpp)
# add antrl4cpp artifacts to project environment
include_directories(${ANTLR4_INCLUDE_DIRS})

# set variable pointing to the antlr tool that supports C++
# this is not required if the jar file can be found under PATH environment
set(ANTLR_EXECUTABLE ${CMAKE_CURRENT_SOURCE_DIR}/../Jars/antlr-4.13.0-complete.jar)
# add macros to generate ANTLR Cpp code from grammar
find_package(ANTLR REQUIRED)

# Call macro to add lexer and grammar to your build dependencies.
antlr_target(GrammarLexer ../Grammar/fcssLexer.g4 LEXER
             PACKAGE antlrcpptest)
antlr_target(GrammarParser ../Grammar/fcssParser.g4 PARSER
             PACKAGE antlrcpptest
             DEPENDS_ANTLR GrammarLexer
             COMPILE_FLAGS -lib ${ANTLR_GrammarLexer_OUTPUT_DIR})

# include generated files in project environment
include_directories(${ANTLR_GrammarLexer_OUTPUT_DIR})
include_directories(${ANTLR_GrammarParser_OUTPUT_DIR})

# add generated grammar to demo binary target
add_executable(compiler main.cpp
               ${ANTLR_GrammarLexer_CXX_OUTPUTS}
               ${ANTLR_GrammarParser_CXX_OUTPUTS})
target_link_libraries(compiler antlr4_static)
