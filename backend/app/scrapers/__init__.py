import hishel.httpx
import httpx
from httpx_retries import Retry, RetryTransport


def build_transport() -> httpx.AsyncBaseTransport:
    """Cria o transport HTTP usado pelos scrapers.

    Um novo transport deve ser criado para cada `httpx.AsyncClient`: ao sair
    do `async with`, o client fecha o transport (e o storage do cache), que
    então não pode mais ser reutilizado nas próximas sincronizações.
    """
    # Retry para lidar com falhas temporárias da API (ex: 500, 502, etc.)
    retry = Retry(total=5, backoff_factor=0.5)
    retry_transport = RetryTransport(
        httpx.AsyncHTTPTransport(verify=False), retry=retry
    )

    # Cache HTTP para evitar buscar os dados quando não houver mudanças
    return hishel.httpx.AsyncCacheTransport(
        next_transport=retry_transport,
        storage=hishel.AsyncSqliteStorage(),
    )
