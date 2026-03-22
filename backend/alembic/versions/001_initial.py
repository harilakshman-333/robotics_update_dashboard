"""initial

Revision ID: 001_initial
Revises: 
Create Date: 2026-03-22 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'feed_items',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('url', sa.String(), unique=True, nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('source', sa.Enum('x', 'gmail', 'web', name='sourceenum'), nullable=False),
        sa.Column('raw_text', sa.String(), nullable=False),
        sa.Column('summary', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('sentiment', sa.String(), nullable=True),
        sa.Column('entities_json', sa.JSON(), nullable=True),
        sa.Column('relevance_score', sa.Integer(), nullable=True),
        sa.Column('enriched', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('enriched_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('url', name='uq_feeditem_url')
    )

def downgrade():
    op.drop_table('feed_items')
    op.execute('DROP TYPE IF EXISTS sourceenum')
