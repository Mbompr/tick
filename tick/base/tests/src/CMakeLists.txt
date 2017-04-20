add_executable(tick_test_base utils_gtest.cpp)

set(CMAKE_VERBOSE_MAKEFILE ON)



target_link_libraries(tick_test_base
    ${PROJECT_BINARY_DIR}/../${TICKLIB_ARRAY}
    ${PROJECT_BINARY_DIR}/../${TICKLIB_BASE}

    ${TICK_TEST_LIBS}

    )
