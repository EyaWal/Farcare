# FarCare

Outil de suivi et de préparation pour les proches aidants à distance — pour ceux qui vivent loin de parents vieillissants et veulent à la fois garder un œil sur leur bien-être et se préparer aux imprévus.

## Le problème
Vivre loin de ses parents qui vieillissent pose deux inquiétudes : savoir si tout va bien au quotidien, et être prête financièrement en cas d'imprévu (santé notamment). Les outils existants sont soit des applis médicales pour professionnels, soit des simulateurs financiers génériques — rien ne connecte les deux pour un aidant à distance non-spécialiste.

## Fonctionnalités prévues
- **Suivi & info** : check-ins réguliers simples, historique visuel, détection d'anomalies (patterns inhabituels)
- **Préparation financière** : simulation Monte Carlo pour dimensionner un fonds d'urgence adapté au risque santé à l'international

## Stack technique
- Backend : FastAPI
- Base de données : SQLite (dev) / PostgreSQL (prod)
- Data/ML : NumPy, SciPy, scikit-learn, pandas
- Interface : à définir (Streamlit ou templates Jinja2)

## Statut
🚧 En cours de développement (squelette initial posé).

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
