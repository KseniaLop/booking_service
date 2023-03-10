"""empty message

Revision ID: d604a28a1a96
Revises: 6d39bc64b876
Create Date: 2023-01-30 15:05:08.403795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd604a28a1a96'
down_revision = '6d39bc64b876'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('film', schema=None) as batch_op:
        batch_op.add_column(sa.Column('free_sits_count', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('price', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('film', schema=None) as batch_op:
        batch_op.drop_column('price')
        batch_op.drop_column('free_sits_count')

    # ### end Alembic commands ###
