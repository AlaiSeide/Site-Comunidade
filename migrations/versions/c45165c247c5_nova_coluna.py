"""nova coluna

Revision ID: c45165c247c5
Revises: 56b4dfbe4769
Create Date: 2024-10-21 00:26:59.607356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c45165c247c5'
down_revision = '56b4dfbe4769'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ultimo_envio_confirmacao', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_column('ultimo_envio_confirmacao')

    # ### end Alembic commands ###