add_executable(tick_test_model models_gtest.cpp hawkes_models_gtests.cpp)

target_link_libraries(tick_test_model
    ${TICK_TEST_LIBS}
    ${PROJECT_BINARY_DIR}/../${TICKLIB_ARRAY}
    ${PROJECT_BINARY_DIR}/../${TICKLIB_BASE}
    ${PROJECT_BINARY_DIR}/../${TICKLIB_MODEL})
