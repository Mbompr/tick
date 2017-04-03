add_executable(tick_test_base utils_gtest.cpp)

target_link_libraries(tick_test_base
    ${TICK_TEST_LIBS}
    ${PROJECT_BINARY_DIR}/../${TICKLIB_ARRAY}
    ${PROJECT_BINARY_DIR}/../${TICKLIB_BASE})
