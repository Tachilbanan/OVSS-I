"""视频新增播放数

Revision ID: b045c2c510cf
Revises: 541d5f7cbd52
Create Date: 2017-11-15 17:27:07.788389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b045c2c510cf'
down_revision = '541d5f7cbd52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('view', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('videos', 'view')
    # ### end Alembic commands ###
