# Exoplanet Finder

This repository contains a Python script to parse out all the Exoplanets in the
OpenExplanetCatalogue found https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue/
and evaluate their average temperature to find out if they are habitable.

Currently it's just using the mass of their sun and the semi major axis of their orbit to
plus an identical greenhouse effect and albedo of the Earth to calculate this number.

## Steps to run

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python3 app.py`