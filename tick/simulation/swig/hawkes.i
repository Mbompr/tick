
%{
#include "hawkes.h"
%}


class Hawkes : public PP {
 public :

  Hawkes(int dimension, int seed = -1);

  void set_kernel(unsigned int i, unsigned int j, std::shared_ptr<HawkesKernel> kernel);

  void set_mu(unsigned int i, double mu);
  void set_mu(unsigned int i, ArrayDouble &times, ArrayDouble &values);
  void set_mu(unsigned int i, TimeFunction time_function);
};

TICK_MAKE_PICKLABLE(Hawkes, 0);
