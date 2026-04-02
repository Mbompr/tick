#include <memory>
#include <vector>

#include <pybind11/pybind11.h>

#include "common/tick_pybind11_arrays.h"
#include "tick/preprocessing/longitudinal_features_lagger.h"
#include "tick/preprocessing/sparse_longitudinal_features_product.h"

namespace py = pybind11;

PYBIND11_MODULE(preprocessing, m) {
  tick::pybind::ensure_numpy_imported();

  m.doc() = "tick.preprocessing pybind11 bindings";

  auto load_features = [](py::iterable features) {
    SBaseArrayDouble2dPtrList1D converted;
    for (py::handle item : features) {
      converted.push_back(item.cast<SBaseArrayDouble2dPtr>());
    }
    return converted;
  };

  auto lagger =
      py::class_<LongitudinalFeaturesLagger,
                 std::shared_ptr<LongitudinalFeaturesLagger>>(
          m, "LongitudinalFeaturesLagger")
          .def(py::init([&load_features](py::iterable features,
                                         SArrayULongPtr n_lags) {
                 return std::make_shared<LongitudinalFeaturesLagger>(
                     load_features(features), n_lags);
               }),
               py::arg("features"), py::arg("n_lags"))
          .def("dense_lag_preprocessor",
               &LongitudinalFeaturesLagger::dense_lag_preprocessor,
               py::arg("features"), py::arg("out"), py::arg("censoring"))
          .def("sparse_lag_preprocessor",
               &LongitudinalFeaturesLagger::sparse_lag_preprocessor,
               py::arg("row"), py::arg("col"), py::arg("data"),
               py::arg("out_row"), py::arg("out_col"), py::arg("out_data"),
               py::arg("censoring"));

  auto product =
      py::class_<SparseLongitudinalFeaturesProduct,
                 std::shared_ptr<SparseLongitudinalFeaturesProduct>>(
          m, "SparseLongitudinalFeaturesProduct")
          .def(py::init([&load_features](py::iterable features) {
                 return std::make_shared<SparseLongitudinalFeaturesProduct>(
                     load_features(features));
               }),
               py::arg("features"))
          .def("sparse_features_product",
               &SparseLongitudinalFeaturesProduct::sparse_features_product,
               py::arg("row"), py::arg("col"), py::arg("data"),
               py::arg("out_row"), py::arg("out_col"), py::arg("out_data"));
}
