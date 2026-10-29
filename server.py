"""Portal Luz do Bairro - API minima usada no Lab do Modulo 9 (200DEV).

Somente biblioteca padrao: o build nao depende de pip nem de acesso a PyPI.
Variaveis de ambiente (vindas do ConfigMap gerado pelo Kustomize):
  APP_VERSION  versao exibida em "/" (o pipeline grava o SHA curto do commit)
  APP_ENV      ambiente (dev, prod)
  APP_MESSAGE  mensagem exibida em "/"
  PORT         porta de escuta (padrao 8080)
"""
import json
import os
import socket
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from fatura import calcular_fatura

VERSAO = os.environ.get("APP_VERSION", "dev")
AMBIENTE = os.environ.get("APP_ENV", "local")
MENSAGEM = os.environ.get("APP_MESSAGE", "Portal Luz do Bairro")
PORTA = int(os.environ.get("PORT", "8080"))


class Handler(BaseHTTPRequestHandler):
    server_version = "LuzBairro/1.0"

    def _json(self, status, payload):
        corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            return self._json(200, {
                "app": "luz-bairro",
                "versao": VERSAO,
                "ambiente": AMBIENTE,
                "mensagem": MENSAGEM,
                "pod": socket.gethostname(),
            })
        if url.path in ("/healthz", "/readyz"):
            return self._json(200, {"status": "ok"})
        if url.path == "/fatura":
            consulta = parse_qs(url.query)
            try:
                kwh = float(consulta.get("kwh", ["0"])[0])
                bandeira = consulta.get("bandeira", ["verde"])[0]
                return self._json(200, {"kwh": kwh, "bandeira": bandeira,
                                        "valor": calcular_fatura(kwh, bandeira)})
            except ValueError as erro:
                return self._json(400, {"erro": str(erro)})
        return self._json(404, {"erro": "nao encontrado"})

    def log_message(self, formato, *args):
        # Um log por linha no stdout: aparece em "oc logs" e no console.
        print("%s - %s" % (self.address_string(), formato % args), flush=True)


def criar_servidor(porta=PORTA, host="0.0.0.0"):
    return ThreadingHTTPServer((host, porta), Handler)


if __name__ == "__main__":
    servidor = criar_servidor()
    print("luz-bairro versao=%s ambiente=%s porta=%d" % (VERSAO, AMBIENTE, PORTA), flush=True)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
