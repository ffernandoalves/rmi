Como você estar usando uma quantidade fixa de registros (k), você pode apenas comparar a soma de cada sublista em vez de calcular a média e compara-las, já que fazer divisão tem um certo custo.

```python
def retorna_maior_intervalo_sum2(lista, numero_registros):
    soma_aux = sum(lista[:numero_registros])
    soma = soma_aux
    inicio_maior = 0
    for x in range(1, len(lista)-numero_registros+1):
        soma_aux = soma_aux - lista[x-1] + lista[x+numero_registros-1]
        if soma_aux > soma:
            inicio_maior = x
            soma = soma_aux
    return soma/numero_registros, inicio_maior, inicio_maior + numero_registros - 1
```

Vou estar usando a resposta do @[hkotsubo](https://pt.stackoverflow.com/users/112052/hkotsubo "66.416 reputação") nesse [link](https://ideone.com/69O4nQ) e os demais comentários como base para testar o tempo de execução.

Vou usar a seguinte `lista` para forçar sempre a execução do que tem dentro do `if` para toda sublista, apenas para usar a máxima capacidade:
```python
gera_lista = lambda N: list(range(1, N+1))
lista = gera_lista(1_000_000) # -> sempre a maior média/soma, a cada sublista, estará no fim da lista
lista.reverse() # -> sempre a maior média/soma, a cada sublista, estará no inicio da lista
```

Comparando com a função `retorna_maior_intervalo_sum` [aqui](https://ideone.com/69O4nQ), pois é a que possuí o melhor tempo:
```python
# input
lista = gera_lista(1_000_000)
params = { 'number': 100, 'globals': globals() }
print('{:.<12} {}'.format('sum', timeit('retorna_maior_intervalo_sum(lista, 3)', **params)))
print('{:.<12} {}'.format('sum2', timeit('retorna_maior_intervalo_sum2(lista, 3)', **params)))
```

```bash
# output
sum......... 24.89773669999704
sum2........ 14.929011599997466
```

Como um adicional, Python puro e performance não costumam andar muito juntos. Então por motivos de curiosidade implementei a função `retorna_maior_intervalo_sum2` usando CPython em C++.

_PS: Nessa implementação aceita apenas valores inteiros._

```c++
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <iostream>
#include <vector>

typedef long int tp_list;
typedef unsigned long int tp_index;

void max_mean(std::vector<tp_list>& arr, double& mean, tp_index& start_id, tp_index& end_id, tp_index n, tp_index k) {
    if (n < k) return;

    double sum_aux = 0;

    for (tp_index i = 0; i < k; ++i) {
        sum_aux += static_cast<double>(arr[i]);
    }

    double sum = sum_aux;

    start_id = 0;
    end_id = k - 1;

    for (tp_index x = 1; x <= n - k; ++x) {
        sum_aux = sum_aux - static_cast<double>(arr[x - 1]) + static_cast<double>(arr[x + k-1]);
        if (sum_aux > sum) {
            sum = sum_aux;
            start_id = x;
            end_id = x + k - 1;
        }
    }
    mean = sum/k;
}

static PyObject *retorna_maior_intervalo(PyObject *self, PyObject *args) {
    PyObject* k_obj = Py_None;
    PyObject* lista_obj = Py_None;

    if (!PyArg_ParseTuple(args, "O!O", &PyList_Type, &lista_obj, &k_obj)) {
        return nullptr;
    }

    if(!PyLong_Check(k_obj)) {
        return PyErr_Format(PyExc_TypeError, "O paramentro k deve ser do tipo inteiro >=1, no entanto foi dado %s", Py_TYPE(k_obj)->tp_name);
    }

    tp_index k = PyLong_AsUnsignedLong(k_obj);
    if(k == static_cast<tp_index>(-1) && PyErr_Occurred()) {
        PyErr_Clear();
        return PyErr_Format(PyExc_TypeError, "O paramentro k deve ser do tipo inteiro >=1, no entanto foi dado %lld", PyLong_AsLongLong(k_obj));
    }

    if (k < 1) {
        PyErr_SetString(PyExc_ValueError, "O parametro \"k\" deve ser um inteiro >=1.");
        return nullptr;
    }

    std::vector<tp_list> lista;
    Py_ssize_t lista_tam = PyList_Size(lista_obj);

    for (Py_ssize_t i = 0; i < lista_tam; ++i) {
        PyObject* value = PyList_GetItem(lista_obj, i);
        if(!PyLong_Check(value)) {
            PyErr_Clear();
            return PyErr_Format(PyExc_TypeError, "A lista deve ter valores do tipo int, no entanto foi dado %s", Py_TYPE(value)->tp_name);
        }
        lista.push_back(PyLong_AsLong(value));
    }

    tp_index n = static_cast<tp_index>(lista.size());
    double mean = -1;
    tp_index start_id = 0;
    tp_index end_id = 0;

    max_mean(lista, mean, start_id, end_id, n, k);

    return Py_BuildValue("dII", mean, start_id, end_id);
}

//===================PYTHON_MODULE_DEFINITION==========================

static PyMethodDef methdef = {
        .ml_name = "retorna_maior_intervalo",
        .ml_meth = static_cast<PyCFunction>(retorna_maior_intervalo),
        .ml_flags = METH_VARARGS,
        .ml_doc = PyDoc_STR(
            "Encontra a maior média a cada \"k\" termos em sequência.\n"
            "\tlista: sequência do tipo int\n"
            "\tk: quantidade (int >= 1) de termos para se calcular a média em sequência\n"
        )
};

static PyMethodDef all_methods[] = {
    methdef,
    {nullptr, nullptr, 0, nullptr} /* Sentinel */
};

static PyModuleDef c_rmi_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "c_rmi",
    .m_size = -1,
    .m_methods = all_methods
};

PyMODINIT_FUNC PyInit_c_rmi(void){
    Py_Initialize();
    return PyModule_Create(&c_rmi_module);
}
```

A função `retorna_maior_intervalo_original`, é a função dada de exemplo na pergunta.

```python
# input
lista = gera_lista(1_000_000)
params = {'number': 100, 'globals': globals()}
fmt = "{:.<12} {}".format
print(fmt('original', timeit('retorna_maior_intervalo_original(lista, 3)', **params)))
print(fmt('sum', timeit('retorna_maior_intervalo_sum(lista, 3)', **params)))
print(fmt('sum2', timeit('retorna_maior_intervalo_sum2(lista, 3)', **params)))
print(fmt('cpython', timeit('rmi.retorna_maior_intervalo(lista, 3)', **params)))
```

```bash
# output
original.... 574.7887451999995
sum......... 25.224075600002834
sum2........ 15.296571599996241
cpython..... 1.1160187000059523
```

---
Pode-se encontrar [aqui](http://github.com/ffernandoalves/rmi) os testes feito, assim como a implementação do código CPython.