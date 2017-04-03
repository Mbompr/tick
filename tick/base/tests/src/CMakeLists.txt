add_executable(tick_test_base utils_gtest.cpp)


set(LIBPATHTICKBASE /Users/svp/Projects/tick-272/build/lib.macosx-10.11-x86_64-3.4/tick/base/build/_base.so)
target_link_libraries(tick_test_base ${GTEST_BOTH_LIBRARIES} ${CMAKE_THREAD_LIBS_INIT} ${EXTRA_TEST_LIBS} ${LIBPATHTICKBASE})
