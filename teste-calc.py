import io
import unittest
from contextlib import redirect_stdout
from fractions import Fraction
from unittest.mock import patch

import calc


def F(x, y=1):
    return Fraction(x, y)


def executar_sistema(entradas):
    """Executa resolver_sistema() com as entradas do teclado e devolve a saída."""
    buffer = io.StringIO()
    with patch("builtins.input", side_effect=[str(e) for e in entradas]), redirect_stdout(buffer):
        calc.resolver_sistema()
    return buffer.getvalue()


class TestSoma(unittest.TestCase):
    def test_soma_2x2(self):
        a = [[F(1), F(2)], [F(3), F(4)]]
        b = [[F(5), F(6)], [F(7), F(8)]]
        self.assertEqual(calc.somar(a, b), [[F(6), F(8)], [F(10), F(12)]])

    def test_soma_com_negativos_e_fracoes(self):
        a = [[F(1, 2), F(-3)]]
        b = [[F(1, 2), F(3)]]
        self.assertEqual(calc.somar(a, b), [[F(1), F(0)]])

    def test_soma_nao_altera_as_matrizes_originais(self):
        a = [[F(1)]]
        b = [[F(2)]]
        calc.somar(a, b)
        self.assertEqual(a, [[F(1)]])
        self.assertEqual(b, [[F(2)]])


class TestMultiplicacaoEscalar(unittest.TestCase):
    def test_escalar_inteiro(self):
        a = [[F(1), F(3)], [F(2), F(4)]]
        self.assertEqual(calc.multiplicar_escalar(F(2), a), [[F(2), F(6)], [F(4), F(8)]])

    def test_escalar_fracionario(self):
        a = [[F(2), F(4)]]
        self.assertEqual(calc.multiplicar_escalar(F(1, 2), a), [[F(1), F(2)]])

    def test_escalar_zero_gera_matriz_nula(self):
        a = [[F(5), F(-7)]]
        self.assertEqual(calc.multiplicar_escalar(F(0), a), [[F(0), F(0)]])


class TestMultiplicacao(unittest.TestCase):
    def test_produto_2x2(self):
        a = [[F(1), F(2)], [F(3), F(4)]]
        b = [[F(5), F(6)], [F(7), F(8)]]
        self.assertEqual(calc.multiplicar(a, b), [[F(19), F(22)], [F(43), F(50)]])

    def test_produto_retangular_2x3_por_3x2(self):
        a = [[F(1), F(2), F(3)], [F(4), F(5), F(6)]]
        b = [[F(7), F(8)], [F(9), F(10)], [F(11), F(12)]]
        self.assertEqual(calc.multiplicar(a, b), [[F(58), F(64)], [F(139), F(154)]])

    def test_resultado_tem_linhas_de_a_e_colunas_de_b(self):
        a = [[F(1), F(2), F(3)]]          # 1 x 3
        b = [[F(1)], [F(2)], [F(3)]]      # 3 x 1
        resultado = calc.multiplicar(a, b)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(len(resultado[0]), 1)
        self.assertEqual(resultado, [[F(14)]])

    def test_matriz_identidade_nao_altera(self):
        a = [[F(2), F(-1)], [F(0), F(5)]]
        i = [[F(1), F(0)], [F(0), F(1)]]
        self.assertEqual(calc.multiplicar(a, i), a)
        self.assertEqual(calc.multiplicar(i, a), a)


class TestTransposta(unittest.TestCase):
    def test_transposta_retangular(self):
        a = [[F(1), F(2), F(3)], [F(4), F(5), F(6)]]
        self.assertEqual(calc.transpor(a), [[F(1), F(4)], [F(2), F(5)], [F(3), F(6)]])

    def test_transposta_de_linha_vira_coluna(self):
        self.assertEqual(calc.transpor([[F(1), F(2)]]), [[F(1)], [F(2)]])

    def test_transposta_da_transposta_e_a_original(self):
        a = [[F(1), F(2)], [F(3), F(4)], [F(5), F(6)]]
        self.assertEqual(calc.transpor(calc.transpor(a)), a)


class TestInversa(unittest.TestCase):
    def test_inversa_2x2(self):
        a = [[F(1), F(2)], [F(3), F(4)]]
        self.assertEqual(calc.inversa(a), [[F(-2), F(1)], [F(3, 2), F(-1, 2)]])

    def test_a_vezes_inversa_e_identidade(self):
        a = [[F(2), F(1), F(1)], [F(1), F(3), F(2)], [F(1), F(0), F(0)]]
        inv = calc.inversa(a)
        self.assertIsNotNone(inv)
        identidade = [[F(1) if i == j else F(0) for j in range(3)] for i in range(3)]
        self.assertEqual(calc.multiplicar(a, inv), identidade)

    def test_inversa_da_identidade_e_identidade(self):
        i = [[F(1), F(0)], [F(0), F(1)]]
        self.assertEqual(calc.inversa(i), i)

    def test_matriz_singular_nao_tem_inversa(self):
        a = [[F(1), F(2)], [F(2), F(4)]]
        self.assertIsNone(calc.inversa(a))

    def test_matriz_nula_nao_tem_inversa(self):
        a = [[F(0), F(0)], [F(0), F(0)]]
        self.assertIsNone(calc.inversa(a))


class TestSistemaLinear(unittest.TestCase):
    def test_spd_solucao_unica(self):
        # x + y = 3 ; x - y = 1  ->  x = 2, y = 1
        saida = executar_sistema([2, 2, 1, 1, 3, 1, -1, 1])
        self.assertIn("SPD", saida)
        self.assertIn("x1 = 2", saida)
        self.assertIn("x2 = 1", saida)

    def test_spd_solucao_fracionaria(self):
        # x + y + z = 6 ; 2x - y + z = 0 ; x + y + 3z = 1  ->  11/3, 29/6, -5/2
        saida = executar_sistema([3, 3, 1, 1, 1, 6, 2, -1, 1, 0, 1, 1, 3, 1])
        self.assertIn("SPD", saida)
        self.assertIn("x1 = 11/3", saida)
        self.assertIn("x2 = 29/6", saida)
        self.assertIn("x3 = -5/2", saida)

    def test_spi_infinitas_solucoes(self):
        # x + y = 2 ; 2x + 2y = 4
        saida = executar_sistema([2, 2, 1, 1, 2, 2, 2, 4])
        self.assertIn("SPI", saida)
        self.assertIn("grau de liberdade = 1", saida)
        self.assertIn("x2 = livre", saida)
        self.assertIn("x1 = 2 - 1*x2", saida)

    def test_si_sem_solucao(self):
        # x + y = 1 ; x + y = 2
        saida = executar_sistema([2, 2, 1, 1, 1, 1, 1, 2])
        self.assertIn("SI", saida)
        self.assertIn("não há solução", saida)
        self.assertNotIn("SPD", saida)
        self.assertNotIn("SPI", saida)

    def test_sistema_com_mais_equacoes_que_incognitas_consistente(self):
        # x = 1 ; y = 2 ; x + y = 3
        saida = executar_sistema([3, 2, 1, 0, 1, 0, 1, 2, 1, 1, 3])
        self.assertIn("SPD", saida)
        self.assertIn("x1 = 1", saida)
        self.assertIn("x2 = 2", saida)


class TestFormatacao(unittest.TestCase):
    def test_inteiro_sem_denominador(self):
        self.assertEqual(calc.fmt(F(4)), "4")

    def test_fracao(self):
        self.assertEqual(calc.fmt(F(-3, 2)), "-3/2")


if __name__ == "__main__":
    unittest.main(verbosity=2)