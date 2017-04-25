#include <gtest/gtest.h>
#include <hawkes.h>

class SimuHawkesTest : public ::testing::Test {
 protected:
  HawkesKernel0 hawkes_kernel_time_func;
  ArrayDouble timestamps;

  std::array<double, 6> test_times{{1., 2., 3.5, 5., 8., 100.}};

  void SetUp() override {
    timestamps = ArrayDouble {0.31, 0.93, 1.29, 2.32, 4.25};
  }
};

TEST_F(SimuHawkesTest, constant_baseline) {
  Hawkes hawkes(1);
  hawkes.set_mu(0, 5.);
  const double simu_time = 10;
  hawkes.simulate(simu_time);
  EXPECT_EQ(hawkes.get_time(), simu_time);
  EXPECT_GT(hawkes.get_n_total_jumps(), 1);
}

TEST_F(SimuHawkesTest, tuple_baseline) {
  ArrayDouble t_values {1., 2., 4., 5.3};
  ArrayDouble y_values {1., 3., 2., 0.};
  Hawkes hawkes(1);
  hawkes.set_mu(0, t_values, y_values);
  const double simu_time = 100;
  hawkes.simulate(simu_time);
  EXPECT_EQ(hawkes.get_time(), simu_time);
  EXPECT_GT(hawkes.get_n_total_jumps(), 1);
  // Check that intensity TimeFunction is cycled
  EXPECT_GT(hawkes.timestamps[0]->last(), 10);
}