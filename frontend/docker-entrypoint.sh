#!/bin/sh
# Executado pelo entrypoint oficial do nginx antes de iniciar o servidor.
# Grava a URL da API em config.js para que a mesma imagem funcione com
# qualquer API, sem precisar de um novo build.
set -eu

if [ -n "${NEXT_PUBLIC_API_URL:-}" ]; then
    printf 'window.__VAGAS_CONFIG__ = { apiUrl: "%s" };\n' \
        "${NEXT_PUBLIC_API_URL%/}" > /usr/share/nginx/html/config.js
    echo "vagas-ui: API configurada em ${NEXT_PUBLIC_API_URL}"
fi
