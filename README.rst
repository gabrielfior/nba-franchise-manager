=====================
nba-franchise-manager
=====================


Development work for Master Thesis in Software Engineering in Oxford.
Goal is to simulate 5 NBA seasons and assess which type of contribution (draft pick, trade, existing player in roster)
is more valuable for winning championships.

Getting started
================

1. Install dependencies
pip install -r requirements.txt

2. Create initial tables
alembic ...

3. Fill initial data
python run_initial_data.py

4. Run simulations




Description
===========

Ideas regarding reporting:
- We could calculate the impact of a player by his win-shares, so for instance, if San Antonio won the championship, we could check how many win-shares came from previous players in the roster, how many from draft picks and how many from traded players.


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.0.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
