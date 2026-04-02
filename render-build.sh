#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# EJECUTAR CARGA DE CATEGORÍAS Y ADMIN
python create_admin.py
python setup_db.py