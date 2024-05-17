import numpy as np
import rmi

K = 3

# lista 1
LISTA_1 = [100, 100, 110, 130, 108, 100, 133, 142, 0, 113]
MEAN_1 = 125.0
START_ID_1 = 5
END_ID_1 = 7
FULL_RESULT_1 = [MEAN_1, START_ID_1, END_ID_1]

# lista 2
LISTA_2 = [1, 2, 3]
MEAN_2 = 2.0
START_ID_2 = 0
END_ID_2 = 2
FULL_RESULT_2 = [MEAN_2, START_ID_2, END_ID_2]

moderate_tolerance = 1e-3
precision = 1e-9
check_type = lambda a, b: isinstance(a, type(b))

res_l1 = rmi.retorna_maior_intervalo(LISTA_1, K)
res_l2 = rmi.retorna_maior_intervalo(LISTA_2, K)

class TestCPython:

    def test_cpython_l1_weak(self):
        # checagem básica de tamanho e igualdade entre o 
        # resultado do cpython e FULL_RESULT_1
        assert(len(res_l1) == len(FULL_RESULT_1))
        assert(np.isclose(FULL_RESULT_1, res_l1, rtol=moderate_tolerance).all())

    def test_cpython_l1_index(self):
        assert(check_type(FULL_RESULT_1[1], 1))
        
        # `start_id` e `end_id` devem ser do tipo int
        assert(check_type(res_l1[1], FULL_RESULT_1[1]))
        assert(check_type(res_l1[2], FULL_RESULT_1[2]))
        
        # compara se `start_id` e `end_id` do cpython 
        # é o mesmo de FULL_RESULT_1
        assert(np.isclose(FULL_RESULT_1[1:], res_l1[1:], rtol=1e0, atol=0e0).all())
        
    def test_cpython_l1_precision(self):
        # desde que o tipo de `mean` do cpython e de FULL_RESULT_1 sejam iguais, ok
        assert(check_type(res_l1[0], FULL_RESULT_1[0]))
        # uma precisão alta, caso seja utilizado um calculo de média diferente
        assert(np.isclose(FULL_RESULT_1[0], res_l1[0], rtol=precision).all())

    def test_cpython_l2_strong(self):
        assert(len(res_l2) == len(FULL_RESULT_2))
        assert(check_type(res_l2[0], FULL_RESULT_2[0]))
        assert(check_type(res_l2[1], FULL_RESULT_2[1]))
        assert(check_type(res_l2[2], FULL_RESULT_2[2]))
        assert(np.isclose(FULL_RESULT_2[0], res_l2[0], rtol=precision).all())
        assert(np.isclose(FULL_RESULT_2[1:], res_l2[1:], rtol=1e0, atol=0e0).all())
