"""empty message

Revision ID: 799076cfb84e
Revises: 0caabbfaa9b6
Create Date: 2022-11-29 21:12:32.065656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '799076cfb84e'
down_revision = '0caabbfaa9b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.alter_column('userid',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=60),
               existing_nullable=False)
        batch_op.create_unique_constraint(batch_op.f('uq_user_userid'), ['userid'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_userid'), type_='unique')
        batch_op.alter_column('userid',
               existing_type=sa.String(length=60),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.drop_column('id')

    # ### end Alembic commands ###
