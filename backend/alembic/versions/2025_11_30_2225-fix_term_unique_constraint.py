"""Fix term unique constraint to include language

Revision ID: fix_term_lang_unique
Revises: a7b3c4d5e6f7
Create Date: 2025-11-30 22:25:45

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fix_term_lang_unique'
down_revision = 'a7b3c4d5e6f7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop old unique constraint on term column
    op.drop_index('ix_terms_term', table_name='terms')
    
    # Recreate index without unique constraint
    op.create_index('ix_terms_term', 'terms', ['term'], unique=False)
    
    # Add new unique constraint on (term, language) combination
    op.create_unique_constraint('uq_term_language', 'terms', ['term', 'language'])


def downgrade() -> None:
    # Remove composite unique constraint
    op.drop_constraint('uq_term_language', 'terms', type_='unique')
    
    # Drop non-unique index
    op.drop_index('ix_terms_term', table_name='terms')
    
    # Recreate unique index on term column only
    op.create_index('ix_terms_term', 'terms', ['term'], unique=True)
