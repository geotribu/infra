# Gestion de l'import des images

Prérequis :

- Python 3.8+
- accès réseau à `https://api.tinify.com:443`

## Compression des images

Nous utilisons le service Tinify via son API REST pour redimensionner les images à une largeur maximale de 1 000 pixels et les compresser.

### Installation

```bash
python3 -m pip install -U pip setuptools wheel
python3 -m pip install -U -r requirements.txt
```

### Usage

1. Stocker la [clé d'API](https://tinify.com/dashboard/api) dans la variable d'environnement `TINIFY_API_KEY`.
1. Optionnellement, régler la limite mensuelle d'appels API à ne pas dépasser dans la variable d'environnement `TINIFY_API_LIMIT` (valeur par défaut : 500).
1. Ajuster les paramètres dans le script :
    - chemin du dossier contenant les images à compresser
    - chemin du dossier où stocker les images compressées
1. Exécuter le script :

    ```bash
    python3 images_uploader/compressor.py
    ```
