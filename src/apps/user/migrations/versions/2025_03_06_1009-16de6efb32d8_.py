"""empty message

Revision ID: 16de6efb32d8
Revises: dd5678e3ecf6
Create Date: 2025-03-06 10:09:09.131518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = '16de6efb32d8'
down_revision: Union[str, None] = 'dd5678e3ecf6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SOCIAL_NETWORKS = ["vk", "twitter", "telegram", "instagram"]


def upgrade() -> None:
    connection = op.get_bind()
    for name in SOCIAL_NETWORKS:
        connection.execute(
            sa.text("INSERT INTO platforms (id, name) VALUES (:id, :name)"),
            {"id": str(uuid.uuid4()), "name": name},
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    connection = op.get_bind()
    for name in SOCIAL_NETWORKS:
        connection.execute(
            sa.text("DELETE FROM platforms WHERE name = :name"),
            {"name": name},
        )
    # ### end Alembic commands ###
