import json
import threading
import unittest
import urllib.error
import urllib.request

import server


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = server.criar_servidor(porta=0, host="127.0.0.1")
        cls.base = "http://127.0.0.1:%d" % cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def get(self, caminho):
        try:
            with urllib.request.urlopen(self.base + caminho, timeout=5) as resposta:
                return resposta.status, json.load(resposta)
        except urllib.error.HTTPError as erro:
            with erro:
                return erro.code, json.load(erro)

    def test_raiz_informa_versao_e_ambiente(self):
        status, dados = self.get("/")
        self.assertEqual(status, 200)
        self.assertEqual(dados["app"], "luz-bairro")
        for campo in ("versao", "ambiente", "mensagem", "pod"):
            self.assertIn(campo, dados)

    def test_probes(self):
        for caminho in ("/healthz", "/readyz"):
            status, dados = self.get(caminho)
            self.assertEqual((status, dados["status"]), (200, "ok"))

    def test_fatura(self):
        status, dados = self.get("/fatura?kwh=100&bandeira=amarela")
        self.assertEqual(status, 200)
        self.assertEqual(dados["valor"], 97.0)

    def test_fatura_bandeira_invalida(self):
        status, dados = self.get("/fatura?kwh=10&bandeira=roxa")
        self.assertEqual(status, 400)
        self.assertIn("erro", dados)

    def test_caminho_inexistente(self):
        status, _ = self.get("/nao-existe")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
