"""fix level of linkedin jobs

O scraper do LinkedIn gravava o nível a partir do filtro `f_E` da busca, que
a busca pública ignora: todas as vagas acabavam como "estagio". Recalcula o
nível a partir do título, com a mesma regra de `app.utils.get_level_seniority`.

Revision ID: 5f2a9c1e7b44
Revises: d41e7c3b9a10
Create Date: 2026-11-13 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f2a9c1e7b44'
down_revision: Union[str, Sequence[str], None] = 'd41e7c3b9a10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Cópia da regra de get_level_seniority (migrations não devem depender do
# código da aplicação, que pode mudar depois).
LEVELS = [
    ('estagio', {'estágio', 'estagio'}),
    ('junior', {'junior', 'jr', 'júnior'}),
    ('pleno', {'pleno', 'pl'}),
    ('senior', {'senior', 'sr', 'sênior'}),
]


def level_from_title(title: str) -> str | None:
    words = set(title.lower().split())
    for level, keywords in LEVELS:
        if words & keywords:
            return level
    return None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    jobs = sa.table(
        'jobs',
        sa.column('id', sa.Integer),
        sa.column('title', sa.String),
        sa.column('level', sa.String),
        sa.column('source', sa.String),
    )
    rows = conn.execute(
        sa.select(jobs.c.id, jobs.c.title).where(jobs.c.source == 'linkedin')
    ).all()
    for job_id, title in rows:
        conn.execute(
            jobs.update()
            .where(jobs.c.id == job_id)
            .values(level=level_from_title(title or ''))
        )


def downgrade() -> None:
    """Downgrade schema."""
    # Correção de dados: não há como (nem por que) restaurar os valores errados.
