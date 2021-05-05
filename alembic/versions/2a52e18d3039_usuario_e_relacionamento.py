"""usuario e relacionamento

Revision ID: 2a52e18d3039
Revises: 0e57dbfb5c25
Create Date: 2021-05-04 23:28:11.389200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a52e18d3039'
down_revision = '0e57dbfb5c25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('senha', sa.String(), nullable=True),
    sa.Column('telefone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_usuario_id'), ['id'], unique=False)

    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('usuario_id', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_produto_id'), ['id'], unique=False)
        batch_op.create_foreign_key('fk_usuario', 'usuario', ['usuario_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produto', schema=None) as batch_op:
        batch_op.drop_constraint('fk_usuario', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_produto_id'))
        batch_op.drop_column('usuario_id')

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_usuario_id'))

    op.drop_table('usuario')
    # ### end Alembic commands ###
