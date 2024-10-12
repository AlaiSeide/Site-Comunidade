"""first commit

Revision ID: aaf8ad2bb972
Revises: 
Create Date: 2024-10-12 23:39:45.069706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaf8ad2bb972'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contato',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('mensagem', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('senha', sa.String(length=80), nullable=False),
    sa.Column('confirmado', sa.Boolean(), nullable=True),
    sa.Column('data_confirmacao', sa.DateTime(), nullable=True),
    sa.Column('codigo_confirmacao', sa.String(length=6), nullable=False),
    sa.Column('foto_perfil', sa.String(length=50), nullable=False),
    sa.Column('cursos', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=50), nullable=False),
    sa.Column('corpo', sa.Text(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('token_redefinicao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('data_expiracao', sa.DateTime(timezone=True), nullable=False),
    sa.Column('usado', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('token_redefinicao')
    op.drop_table('post')
    op.drop_table('usuario')
    op.drop_table('contato')
    # ### end Alembic commands ###