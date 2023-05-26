"""create teleid table

Revision ID: 5f59bb9f1707
Revises: 
Create Date: 2023-05-25 23:19:07.713038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f59bb9f1707'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('teleid', sa.Column('telegram_id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('faceit_nickname', sa.String(), nullable=False),
                    sa.Column('search_count', sa.Integer(), nullable=False, default='0'))
    pass


def downgrade() -> None:
    op.drop_table('teleid')
    pass
