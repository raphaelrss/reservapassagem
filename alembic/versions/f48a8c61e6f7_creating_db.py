"""creating db

Revision ID: f48a8c61e6f7
Revises: 
Create Date: 2023-09-20 23:52:28.642020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f48a8c61e6f7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aeroporto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('cidade', sa.String(), nullable=True),
    sa.Column('pais', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_aeroporto_id'), 'aeroporto', ['id'], unique=False)
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('sobrenome', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('cpf', sa.String(), nullable=True),
    sa.Column('adm', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuario_id'), 'usuario', ['id'], unique=False)
    op.create_table('voo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('origem_id', sa.Integer(), nullable=True),
    sa.Column('destino_id', sa.Integer(), nullable=True),
    sa.Column('data_hora_partida', sa.DateTime(timezone=True), nullable=True),
    sa.Column('capacidade', sa.Integer(), nullable=True),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.Column('numero_voo', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['destino_id'], ['aeroporto.id'], ),
    sa.ForeignKeyConstraint(['origem_id'], ['aeroporto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_voo_id'), 'voo', ['id'], unique=False)
    op.create_table('reserva',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.Column('voo_id', sa.Integer(), nullable=True),
    sa.Column('data', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['reserva.id'], ),
    sa.ForeignKeyConstraint(['voo_id'], ['voo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reserva_id'), 'reserva', ['id'], unique=False)
    op.create_table('pagamento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reserva_id', sa.Integer(), nullable=True),
    sa.Column('cidade', sa.Float(), nullable=True),
    sa.Column('tipo', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['reserva_id'], ['reserva.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pagamento_id'), 'pagamento', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pagamento_id'), table_name='pagamento')
    op.drop_table('pagamento')
    op.drop_index(op.f('ix_reserva_id'), table_name='reserva')
    op.drop_table('reserva')
    op.drop_index(op.f('ix_voo_id'), table_name='voo')
    op.drop_table('voo')
    op.drop_index(op.f('ix_usuario_id'), table_name='usuario')
    op.drop_table('usuario')
    op.drop_index(op.f('ix_aeroporto_id'), table_name='aeroporto')
    op.drop_table('aeroporto')
    # ### end Alembic commands ###