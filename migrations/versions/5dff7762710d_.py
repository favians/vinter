"""empty message

Revision ID: 5dff7762710d
Revises: ec4719cf3683
Create Date: 2019-11-27 22:26:06.109488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dff7762710d'
down_revision = 'ec4719cf3683'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('description', sa.String(length=2048), nullable=True))
    op.add_column('company', sa.Column('industry', sa.String(length=255), nullable=True))
    op.add_column('company', sa.Column('location', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('company', 'location')
    op.drop_column('company', 'industry')
    op.drop_column('company', 'description')
    # ### end Alembic commands ###