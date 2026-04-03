#include <pybind11/pybind11.h>

#include "common/tick_pybind11_arrays.h"
#include "tick/base_model/model_generalized_linear.h"
#include "tick/base_model/model_lipschitz.h"
#include "tick/linear_model/model_linreg.h"
#include "tick/linear_model/model_logreg.h"
#include "tick/linear_model/model_poisreg.h"

namespace py = pybind11;

namespace {

template <typename ModelType, typename BaseGeneralizedLinear,
          typename BaseLipschitz, typename Array2dPtr, typename ArrayPtr,
          typename Scalar>
void bind_model_glm(py::module_ &m, const char *name) {
  py::class_<ModelType, std::shared_ptr<ModelType>, BaseGeneralizedLinear,
             BaseLipschitz>(m, name)
      .def(py::init<Array2dPtr, ArrayPtr, bool, int>(), py::arg("features"),
           py::arg("labels"), py::arg("fit_intercept"),
           py::arg("n_threads") = 1);
}

template <typename Scalar>
void bind_sigmoid(py::class_<TModelLogReg<Scalar, Scalar>,
                             std::shared_ptr<TModelLogReg<Scalar, Scalar>>,
                             TModelGeneralizedLinear<Scalar, Scalar>,
                             TModelLipschitz<Scalar, Scalar>> &cls) {
  cls.def_static(
      "sigmoid",
      [](const Array<Scalar> &x, Array<Scalar> &out) {
        TModelLogReg<Scalar, Scalar>::sigmoid(x, out);
      },
      py::arg("x"), py::arg("out"));
}

template <typename ModelType, typename BaseGeneralizedLinear, typename Array2dPtr,
          typename ArrayPtr>
void bind_model_poisreg(py::module_ &m, const char *name) {
  py::class_<ModelType, std::shared_ptr<ModelType>, BaseGeneralizedLinear>(
      m, name)
      .def(py::init<Array2dPtr, ArrayPtr, LinkType, bool, int>(),
           py::arg("features"), py::arg("labels"), py::arg("link_type"),
           py::arg("fit_intercept"), py::arg("n_threads") = 1)
      .def("get_link_type", &ModelType::get_link_type)
      .def("set_link_type", &ModelType::set_link_type);
}

}  // namespace

PYBIND11_MODULE(linear_model, m) {
  tick::pybind::ensure_numpy_imported();

  m.doc() = "tick.linear_model pybind11 bindings";

  py::enum_<LinkType>(m, "LinkType")
      .value("LinkType_identity", LinkType::identity)
      .value("LinkType_exponential", LinkType::exponential)
      .export_values();

  bind_model_glm<ModelLinRegDouble, ModelGeneralizedLinearDouble,
                 ModelLipschitzDouble, SBaseArrayDouble2dPtr, SArrayDoublePtr,
                 double>(m, "ModelLinRegDouble");
  bind_model_glm<ModelLinRegFloat, ModelGeneralizedLinearFloat,
                 ModelLipschitzFloat, SBaseArrayFloat2dPtr, SArrayFloatPtr,
                 float>(m, "ModelLinRegFloat");

  auto logreg_double =
      py::class_<ModelLogRegDouble, std::shared_ptr<ModelLogRegDouble>,
                 ModelGeneralizedLinearDouble, ModelLipschitzDouble>(
          m, "ModelLogRegDouble");
  logreg_double
      .def(py::init<SBaseArrayDouble2dPtr, SArrayDoublePtr, bool, int>(),
           py::arg("features"), py::arg("labels"),
           py::arg("fit_intercept"), py::arg("n_threads") = 1);
  bind_sigmoid<double>(logreg_double);

  auto logreg_float = py::class_<ModelLogRegFloat,
                                 std::shared_ptr<ModelLogRegFloat>,
                                 ModelGeneralizedLinearFloat,
                                 ModelLipschitzFloat>(m, "ModelLogRegFloat");
  logreg_float
      .def(py::init<SBaseArrayFloat2dPtr, SArrayFloatPtr, bool, int>(),
           py::arg("features"), py::arg("labels"),
           py::arg("fit_intercept"), py::arg("n_threads") = 1);
  bind_sigmoid<float>(logreg_float);

  bind_model_poisreg<ModelPoisRegDouble, ModelGeneralizedLinearDouble,
                     SBaseArrayDouble2dPtr, SArrayDoublePtr>(
      m, "ModelPoisRegDouble");
  bind_model_poisreg<ModelPoisRegFloat, ModelGeneralizedLinearFloat,
                     SBaseArrayFloat2dPtr, SArrayFloatPtr>(
      m, "ModelPoisRegFloat");
}
