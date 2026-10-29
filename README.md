# luz-bairro-app

API mínima do **Portal Luz do Bairro** (Lab 09 — 200DEV). Só biblioteca padrão do Python 3.

| Rota | Resposta |
|---|---|
| `GET /` | `{"app","versao","ambiente","mensagem","pod"}` |
| `GET /healthz`, `GET /readyz` | `{"status":"ok"}` (probes) |
| `GET /fatura?kwh=100&bandeira=amarela` | `{"kwh","bandeira","valor"}` (bandeira: `verde`, `amarela`, `vermelha`) |

Variáveis de ambiente: `APP_VERSION`, `APP_ENV`, `APP_MESSAGE`, `PORT` (padrão 8080). Em cluster, vêm do ConfigMap gerado pelo repositório de configuração.

```bash
python3 -m unittest -v        # testes (os mesmos que o pipeline roda)
python3 server.py             # http://localhost:8080
```

A imagem é construída pelo pipeline Tekton a partir do `Containerfile` (base UBI 9, usuário não-root).
