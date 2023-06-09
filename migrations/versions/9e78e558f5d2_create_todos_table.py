"""Create todos table

Revision ID: 9e78e558f5d2
Revises:
Create Date: 2023-04-08 23:27:49.189966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02acaa3b707e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=100), nullable=False),
                    sa.Column('description', sa.String(
                        length=200), nullable=True),
                    sa.Column('status', sa.String(length=20), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    # ### end Alembic commands ###
