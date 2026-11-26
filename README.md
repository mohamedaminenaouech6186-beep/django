# Cabinet médical — Atelier 3

Projet Django pour le dashboard Admin. Depuis le dossier contenant manage.py, sous Windows PowerShell :

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/admin/ et se connecter. Créer des médecins, patients et spécialités avant les rendez-vous. Créer au moins trois rendez-vous futurs pour tester la pagination. Tester les filtres, la recherche, les actions et les validations.

Tests : `python manage.py test` et `python manage.py check`.

La base cabinet_medical.sqlite3 est créée localement. Les anciennes bases et le venv ne sont pas inclus. Le projet conserve les noms originaux Specialty, perscription et les valeurs de statut. Les actions utilisent les constantes du modèle. Le secret par défaut est réservé au développement local ; utiliser DJANGO_SECRET_KEY pour un vrai déploiement.

Le cours cible Django 5.2 ; les tests dans le sandbox ont utilisé Django 6.1.3 fourni dans le ZIP initial.
