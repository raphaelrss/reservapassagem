"""add user password

Revision ID: 10394ad20c30
Revises: c6d9b9ab6738
Create Date: 2023-09-25 18:23:47.344581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10394ad20c30'
down_revision: Union[str, None] = 'c6d9b9ab6738'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('hash_password', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'hash_password')
    # ### end Alembic commands ###