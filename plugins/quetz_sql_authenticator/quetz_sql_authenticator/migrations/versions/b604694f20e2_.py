"""empty message

Revision ID: b604694f20e2
Revises:
Create Date: 2022-10-17 16:05:45.154611

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b604694f20e2'
down_revision = None
branch_labels = ('quetz-sql-authenticator',)
depends_on = 'quetz'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'credentials',
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('username'),
    )
    with op.batch_alter_table('channels', schema=None) as batch_op:
        batch_op.alter_column(
            'size',
            existing_type=sa.INTEGER(),
            type_=sa.BigInteger(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            'size_limit',
            existing_type=sa.INTEGER(),
            type_=sa.BigInteger(),
            existing_nullable=True,
        )

    with op.batch_alter_table('package_versions', schema=None) as batch_op:
        batch_op.alter_column(
            'size',
            existing_type=sa.INTEGER(),
            type_=sa.BigInteger(),
            existing_nullable=True,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('package_versions', schema=None) as batch_op:
        batch_op.alter_column(
            'size',
            existing_type=sa.BigInteger(),
            type_=sa.INTEGER(),
            existing_nullable=True,
        )

    with op.batch_alter_table('channels', schema=None) as batch_op:
        batch_op.alter_column(
            'size_limit',
            existing_type=sa.BigInteger(),
            type_=sa.INTEGER(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            'size',
            existing_type=sa.BigInteger(),
            type_=sa.INTEGER(),
            existing_nullable=True,
        )

    op.drop_table('credentials')
    # ### end Alembic commands ###
