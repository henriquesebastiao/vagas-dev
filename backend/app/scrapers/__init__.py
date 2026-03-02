import hishel.httpx
import httpx
from httpx_retries import Retry, RetryTransport

# Configura retry para lidar com falhas temporárias da API (ex: 500, 502, etc.)
_retry = Retry(total=5, backoff_factor=0.5)
_transport = httpx.AsyncHTTPTransport(verify=False)
_retry_transport = RetryTransport(_transport, retry=_retry)

# Cache HTTP para evitar buscar os dados quando não houver mudanças
transport = hishel.httpx.AsyncCacheTransport(
    next_transport=_retry_transport,
    storage=hishel.AsyncSqliteStorage(),
)
