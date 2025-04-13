"""Reconfiguração inicial das migrations

Revision ID: dbb98b0044bf
Revises: 
Create Date: 2025-04-07 17:40:29.614684

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dbb98b0044bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cargo', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('_endereco', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('_permissions', sa.Text(), nullable=True))
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.String(length=255),
               nullable=False)
        batch_op.drop_column('estado')
        batch_op.drop_column('cidade')
        batch_op.drop_column('rua')
        batch_op.drop_column('bairro')
        batch_op.drop_column('cep')
        batch_op.drop_column('complemento')
        batch_op.drop_column('numero')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('numero', mysql.VARCHAR(length=10), nullable=True))
        batch_op.add_column(sa.Column('complemento', mysql.VARCHAR(length=50), nullable=True))
        batch_op.add_column(sa.Column('cep', mysql.VARCHAR(length=8), nullable=True))
        batch_op.add_column(sa.Column('bairro', mysql.VARCHAR(length=50), nullable=True))
        batch_op.add_column(sa.Column('rua', mysql.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('cidade', mysql.VARCHAR(length=50), nullable=True))
        batch_op.add_column(sa.Column('estado', mysql.VARCHAR(length=2), nullable=True))
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=128),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        batch_op.drop_column('_permissions')
        batch_op.drop_column('_endereco')
        batch_op.drop_column('cargo')

    # ### end Alembic commands ###
