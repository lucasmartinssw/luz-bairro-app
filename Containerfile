# Portal Luz do Bairro - imagem de runtime (Modulo 9, 200DEV)
# Base UBI: roda com UID arbitrario do OpenShift (grupo 0) e nao precisa de root.
FROM registry.access.redhat.com/ubi9/python-312:latest

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/app-root/src
COPY server.py fatura.py ./

EXPOSE 8080
CMD ["python3", "server.py"]
