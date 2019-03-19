#include "tiascript.h"
#include "defines.h"
#include "types.h"

static PyObject* App_exit(App *self)
{
  // HRESULT result =

  // self->iface->Exit();
  return NULL;
}


static PyGetSetDef App_getset[] = {
    // {"Cameras",   (getter)&Acquisition_get_Cameras, NULL, NULL, NULL},
    // {"Detectors", (getter)&Acquisition_get_Detectors, NULL, NULL, NULL},
    {NULL}  /* Sentinel */
};

static PyMethodDef App_methods[] = {
    // {"AddDisplayWindow",            (PyCFunction)&Acquisition_AddDisplayWindow, METH_VARARGS, NULL},
    {"Exit",            (PyCFunction)&App_exit, NULL, NULL},
    {NULL}  /* Sentinel */
};

IMPLEMENT_WRAPPER(App, ESVision::IApplication, App_getset, App_methods)
