## Description
Petit script qui tente de trier les offres de stage de l'ETS (https://see.etsmtl.ca/Postes/Affichages) par le rating de chaque compagnie utilisant l'api de Glassdoor.

## Requirements
- Python
- Glassdoor valid api key: https://www.glassdoor.ca/developer

## How to
- Remplir les champs de la section *Settings* du script `ets_jobs_rating.py`

| Setting | Description |
| --- | --- |
| `file_input` | Fichier contenant le json du site d'offre de stage |
| `file_output` | Résultats généré par le script |
| `api_token` | Glassdoor Partner ID |
| `api_token_key` | Glassdoor Key |

- Copier l'array du json accessible dans la page d'offre de stages dans le fichier mentionné dans la variable $file_input.
Celui-ci est accessible en affichant le code source de la page dans un bloc `<script type="text/javascript"></script>` avant la fin du `</body>`
Copier l'array de `{"Records":`(voir le fichier SEE_jobs.json pour un exemple de la structure du JSON). 
- Lancer le script `python ets_jobs_rating.py`
- Les résultats obtenus seront généré dans le fichier $file_output

<a href='https://www.glassdoor.ca/index.htm'>powered by <img src='https://www.glassdoor.com/static/img/api/glassdoor_logo_80.png' title='Job Search' /></a>