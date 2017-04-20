
%{
#include "hawkes.h"
%}


class Hawkes : public PP {
 public :

  Hawkes(int dimension, int seed = -1);

  void set_kernel(int i,int j, std::shared_ptr<HawkesKernel> kernel);

  void set_mu(int i, double mu);
};

TICK_MAKE_PICKLABLE(Hawkes, 0);
