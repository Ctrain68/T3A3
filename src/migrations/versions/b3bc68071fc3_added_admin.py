"""added admin

Revision ID: b3bc68071fc3
Revises: 48ab8d684fea
Create Date: 2020-12-17 18:46:54.188084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3bc68071fc3'
down_revision = '48ab8d684fea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'admin')
    # ### end Alembic commands ###
