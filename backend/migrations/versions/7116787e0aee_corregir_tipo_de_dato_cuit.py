"""Corregir tipo de dato CUIT

Revision ID: 7116787e0aee
Revises: 81bf2471bc33
Create Date: 2025-03-05 15:55:19.235926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7116787e0aee'
down_revision = '81bf2471bc33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cuit', sa.String(length=20), nullable=False))
        batch_op.create_unique_constraint(None, ['cuit'])
        batch_op.drop_column('CUIT')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('CUIT', sa.INTEGER(), server_default=sa.text('0'), nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('cuit')

    # ### end Alembic commands ###
