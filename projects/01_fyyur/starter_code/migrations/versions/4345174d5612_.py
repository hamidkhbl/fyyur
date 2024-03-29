"""empty message

Revision ID: 4345174d5612
Revises: c1a3e93a78a7
Create Date: 2022-10-24 15:16:13.644659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4345174d5612'
down_revision = 'c1a3e93a78a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titile', sa.String(length=30), nullable=False),
    sa.Column('describe', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('looking_for_venues', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.drop_column('Artist', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking_description')
    op.drop_column('Artist', 'looking_for_venues')
    op.drop_column('Artist', 'website_link')
    op.drop_table('Show')
    op.drop_table('Genre')
    # ### end Alembic commands ###
