"""Add password_hash column to user table

Revision ID: 695afe2ced4e
Revises: 
Create Date: 2025-03-16 14:16:22.164499

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '695afe2ced4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Exclui a tabela 'users' se existir
    op.drop_table('users')

    # Adiciona a coluna 'password_hash' à tabela 'user'
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=False))
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('nome',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('bairro',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('cidade',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('estado',
               existing_type=mysql.VARCHAR(length=2),
               nullable=False)

def downgrade():
    # Remove a coluna 'password_hash' da tabela 'user'
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('password_hash')
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('nome',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('bairro',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('cidade',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('estado',
               existing_type=mysql.VARCHAR(length=2),
               nullable=True)

    # Recria a tabela 'users' se necessário
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('password_hash', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=120), nullable=False),
    sa.Column('nome', mysql.VARCHAR(length=120), nullable=False),
    sa.Column('cpf', mysql.VARCHAR(length=11), nullable=False),
    sa.Column('rua', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('numero', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('complemento', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('cep', mysql.VARCHAR(length=8), nullable=False),
    sa.Column('bairro', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('cidade', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('estado', mysql.VARCHAR(length=2), nullable=False),
    sa.Column('setor', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('funcao', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('especialidade', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('registro_categoria', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('telefone', mysql.VARCHAR(length=15), nullable=True),
    sa.Column('data_admissao', sa.DATE(), nullable=True),
    sa.Column('status', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('tipo_acesso', mysql.VARCHAR(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index('username', ['username'], unique=True)
        batch_op.create_index('email', ['email'], unique=True)
        batch_op.create_index('cpf', ['cpf'], unique=True)

    # ### end Alembic commands ###
