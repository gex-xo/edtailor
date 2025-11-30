"""add language field to all content models

Revision ID: a7b3c4d5e6f7
Revises: d03f8623b3fe
Create Date: 2025-11-30 15:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7b3c4d5e6f7'
down_revision: Union[str, None] = 'd03f8623b3fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add language column to categories
    op.add_column('categories', sa.Column('language', sa.String(length=2), nullable=False, server_default='en'))
    op.create_index(op.f('ix_categories_language'), 'categories', ['language'], unique=False)

    # Add language column to topics
    op.add_column('topics', sa.Column('language', sa.String(length=2), nullable=False, server_default='en'))
    op.create_index(op.f('ix_topics_language'), 'topics', ['language'], unique=False)

    # Add language column to lessons
    op.add_column('lessons', sa.Column('language', sa.String(length=2), nullable=False, server_default='en'))
    op.create_index(op.f('ix_lessons_language'), 'lessons', ['language'], unique=False)

    # Add language column to fabrics
    op.add_column('fabrics', sa.Column('language', sa.String(length=2), nullable=False, server_default='en'))
    op.create_index(op.f('ix_fabrics_language'), 'fabrics', ['language'], unique=False)

    # Add language column to garments
    op.add_column('garments', sa.Column('language', sa.String(length=2), nullable=False, server_default='en'))
    op.create_index(op.f('ix_garments_language'), 'garments', ['language'], unique=False)

    # Add language column to terms
    op.add_column('terms', sa.Column('language', sa.String(length=2), nullable=False, server_default='en'))
    op.create_index(op.f('ix_terms_language'), 'terms', ['language'], unique=False)


def downgrade() -> None:
    # Remove language column and index from all tables
    op.drop_index(op.f('ix_terms_language'), table_name='terms')
    op.drop_column('terms', 'language')

    op.drop_index(op.f('ix_garments_language'), table_name='garments')
    op.drop_column('garments', 'language')

    op.drop_index(op.f('ix_fabrics_language'), table_name='fabrics')
    op.drop_column('fabrics', 'language')

    op.drop_index(op.f('ix_lessons_language'), table_name='lessons')
    op.drop_column('lessons', 'language')

    op.drop_index(op.f('ix_topics_language'), table_name='topics')
    op.drop_column('topics', 'language')

    op.drop_index(op.f('ix_categories_language'), table_name='categories')
    op.drop_column('categories', 'language')
