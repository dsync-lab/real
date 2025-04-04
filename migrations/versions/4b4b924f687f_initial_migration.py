"""initial migration

Revision ID: 4b4b924f687f
Revises: 
Create Date: 2024-02-28 19:41:14.426693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b4b924f687f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('property', 'price',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.Integer(),
               existing_nullable=False)
    op.add_column('property_image', sa.Column('mimetype', sa.String(length=50), nullable=False))
    op.alter_column('rent_property', 'price',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.Integer(),
               existing_nullable=False)
    op.add_column('rent_property_image', sa.Column('mimetype', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rent_property_image', 'mimetype')
    op.alter_column('rent_property', 'price',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    op.drop_column('property_image', 'mimetype')
    op.alter_column('property', 'price',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###
