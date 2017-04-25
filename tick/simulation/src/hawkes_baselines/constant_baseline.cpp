#include "constant_baseline.h"

HawkesConstantBaseline::HawkesConstantBaseline(double value) : value(value) { }

double HawkesConstantBaseline::get_value(double t) {
  return value;
}

double HawkesConstantBaseline::get_future_bound(double t) {
  return value;
}
