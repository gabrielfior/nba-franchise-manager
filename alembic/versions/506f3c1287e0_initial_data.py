"""initial data

Revision ID: 506f3c1287e0
Revises: f2874f153848
Create Date: 2021-08-16 09:14:29.840975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import orm

from alembic_helpers import *

revision = '506f3c1287e0'
down_revision = 'f2874f153848'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    input_data = read_initial_data()
    team_dict = get_team_names(input_data)
    short_name_team_dict = get_team_short_names(input_data)
    players = get_players(input_data, team_dict)
    draft_picks = get_draft_picks(input_data, team_dict)

    # game_mapper
    game_mappings = get_game_mappings(short_name_team_dict)
    print('teams: {}'.format([i.short_name for i in team_dict.values()]))
    session.add_all(team_dict.values())
    session.add_all(players)
    session.add_all(draft_picks)
    session.add_all(game_mappings)

    session.commit()


def downgrade():
    op.execute('DELETE FROM {}'.format(Player.__tablename__))
    op.execute('DELETE FROM {}'.format(Team.__tablename__))
    op.execute('DELETE FROM {}'.format(DraftPick.__tablename__))
