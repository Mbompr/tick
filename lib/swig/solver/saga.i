// License: BSD 3 clause

%include "sto_solver.i"

%{
#include "tick/solver/saga.h"
%}

template <class T, class K>
class TSAGA : public TStoSolver<T, K> {
 public:
    TSAGA();

    TSAGA(unsigned long epoch_size,
         T tol,
         RandType rand_type,
         T step,
         int record_every = 1,
         int seed = -1,
         int n_threads = 1);
    void set_step(T step);
};

%template(SAGADouble) TSAGA<double, double>;
typedef TSAGA<double, double> SAGADouble;
TICK_MAKE_TEMPLATED_PICKLABLE(TSAGA, SAGADouble, %arg(double, double));

%template(SAGADoubleAtomicIterate) TSAGA<double, std::atomic<double> >;
typedef TSAGA<double, std::atomic<double> > SAGADoubleAtomicIterate;
TICK_MAKE_TEMPLATED_PICKLABLE(TSAGA, SAGADoubleAtomicIterate, %arg(double, std::atomic<double>));

%template(SAGAFloat) TSAGA<float, float>;
typedef TSAGA<float, float> SAGAFloat;
TICK_MAKE_TEMPLATED_PICKLABLE(TSAGA, SAGAFloat, %arg(float, float));


template <class T, class K>
class AtomicSAGA : public TStoSolver<T, K> {
 public:
    AtomicSAGA();

    AtomicSAGA(
      unsigned long epoch_size,
      T tol,
      RandType rand_type,
      T step,
      int record_every = 1,
      int seed = -1,
      int n_threads = 2
    );
};

%template(AtomicSAGADouble) AtomicSAGA<double, double>;
typedef AtomicSAGA<double, double> AtomicSAGADouble;
TICK_MAKE_TEMPLATED_PICKLABLE(AtomicSAGA, AtomicSAGADouble, %arg(double, double));

%template(AtomicSAGADoubleAtomicIterate) AtomicSAGA<double, std::atomic<double> >;
typedef AtomicSAGA<double, std::atomic<double> > AtomicSAGADoubleAtomicIterate;
TICK_MAKE_TEMPLATED_PICKLABLE(AtomicSAGA, AtomicSAGADoubleAtomicIterate, %arg(double, std::atomic<double>));

%template(AtomicSAGAFloat) AtomicSAGA<float, float>;
typedef AtomicSAGA<float, float> AtomicSAGAFloat;
TICK_MAKE_TEMPLATED_PICKLABLE(AtomicSAGA, AtomicSAGAFloat, %arg(float, float));
