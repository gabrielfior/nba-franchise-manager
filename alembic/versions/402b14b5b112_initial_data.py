"""initial data

Revision ID: 402b14b5b112
Revises: 4af34f0608f0
Create Date: 2021-08-16 20:19:06.933066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import orm

from alembic_helpers import *

revision = '402b14b5b112'
down_revision = '4af34f0608f0'
branch_labels = None
depends_on = None


def upgrade():
    year = 2021
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    input_data = read_initial_data()
    team_dict = get_team_names(input_data)
    players = get_players(input_data, team_dict)
    draft_picks = get_draft_picks(input_data, team_dict, year)

    # game_mapper
    game_mappings = get_game_mappings()

    session.add_all(team_dict.values())
    session.add_all(players)
    session.add_all(draft_picks)
    session.add_all(game_mappings)

    session.commit()


def downgrade():
    op.execute('DELETE FROM {}'.format(Player.__tablename__))
    op.execute('DELETE FROM {}'.format(Team.__tablename__))
    op.execute('DELETE FROM {}'.format(DraftPick.__tablename__))
    op.execute('DELETE FROM {}'.format(GameMapper.__tablename__))