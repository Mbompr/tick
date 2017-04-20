add_executable(tick_test_hawkes
        hawkes_kernel_exp_gtest.cpp
        hawkes_kernel_0_gtest.cpp
        hawkes_kernel_power_law_gtest.cpp
        hawkes_kernel_time_func_gtest.cpp
        hawkes_kernel_sumexp_gtest.cpp
        )

target_link_libraries(tick_test_hawkes
    ${PROJECT_BINARY_DIR}/../${TICKLIB_ARRAY}
    ${PROJECT_BINARY_DIR}/../${TICKLIB_BASE}
    ${PROJECT_BINARY_DIR}/../${TICKLIB_CRANDOM}
    ${PROJECT_BINARY_DIR}/../${TICKLIB_SIMULATION}
    ${TICK_TEST_LIBS}
    )
