# Video Organizer

Application de gestion et organisation de vidéos avec système de tags pour Linux.

## Fonctionnalités

- 📁 **Sélection de dossiers sources** : Choisissez un ou plusieurs dossiers contenant vos vidéos
- 🖼️ **Miniatures automatiques** : Génération automatique de vignettes pour chaque vidéo
- 🏷️ **Système de tags personnalisable** :
  - Tags cliquables pour chaque vidéo
  - Ajout de nouveaux tags à la volée
  - Les 10 tags les plus utilisés en premier, puis ordre alphabétique
- 📊 **Affichage en grille** : Vidéos classées par date d'ajout (plus récentes en premier)
- ✓ **Organisation automatique** : Déplacement des vidéos dans des sous-dossiers basés sur les tags
- 💾 **Sauvegarde automatique** : Configuration et statistiques d'utilisation sauvegardées

## Prérequis

- Python 3.8+
- FFmpeg (pour la génération de miniatures)

### Installation de FFmpeg

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

## Installation

1. Installer les dépendances Python :

```bash
pip install -r requirements.txt
```

Ou avec pip3 :

```bash
pip3 install -r requirements.txt
```

## Utilisation

### Lancement de l'application

```bash
python3 video_organizer.py
```

Ou rendez-le exécutable :

```bash
chmod +x video_organizer.py
./video_organizer.py
```

### Guide d'utilisation

1. **Premier lancement** :
   - Cliquez sur "📁 Sélectionner dossier source" pour choisir un dossier contenant vos vidéos
   - Cliquez sur "📂 Dossier de destination" pour choisir où organiser vos vidéos

2. **Organiser une vidéo** :
   - Les vidéos apparaissent sous forme de tuiles avec miniatures
   - Cochez les tags appropriés pour chaque vidéo
   - Cliquez sur "✓ Valider" pour déplacer la vidéo

3. **Gestion des tags** :
   - Cliquez sur "+ Tag" pour ajouter un nouveau tag
   - Les tags sont automatiquement triés : top 10 utilisés, puis alphabétique
   - Les statistiques d'utilisation sont sauvegardées automatiquement

4. **Organisation des fichiers** :
   - Les vidéos sont déplacées dans : `destination/tag1/tag2/tag3/`
   - Exemple : `destination/indoor/bathroom/bikini/video.mp4`
   - Les tags sont triés alphabétiquement dans le chemin

## Structure des fichiers

- `video_organizer.py` : Application principale
- `video_organizer_config.json` : Configuration (créé automatiquement)
- `~/.cache/video_organizer/thumbnails/` : Cache des miniatures

## Configuration

Le fichier `video_organizer_config.json` contient :

```json
{
  "tags": ["tag1", "tag2", ...],
  "tag_usage": {"tag1": 10, "tag2": 5, ...},
  "source_folders": ["/path/to/videos"],
  "destination_folder": "/path/to/organized",
  "thumbnail_cache": {...}
}
```

## Formats vidéo supportés

- MP4
- AVI
- MOV
- MKV
- WEBM
- FLV
- WMV
- M4V

## Raccourcis et astuces

- Les miniatures sont mises en cache pour un chargement plus rapide
- Vous pouvez ajouter plusieurs dossiers sources
- Les tags peuvent contenir n'importe quel caractère (évitez les caractères spéciaux système)
- Les vidéos avec le même nom sont renommées automatiquement (ajout d'un suffixe)

## Dépannage

### Les miniatures ne se génèrent pas
- Vérifiez que FFmpeg est installé : `ffmpeg -version`
- Vérifiez les permissions du dossier cache

### L'application ne démarre pas
- Vérifiez que PyQt6 est installé : `pip3 show PyQt6`
- Vérifiez la version de Python : `python3 --version` (>= 3.8)

### Erreur lors du déplacement
- Vérifiez les permissions du dossier de destination
- Vérifiez que le dossier de destination est défini et existe

## Licence

MIT
