# Video Organizer - Démarrage Rapide

## Installation en 3 étapes

### 1. Installer FFmpeg (requis)

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

### 2. Installer les dépendances Python

```bash
./install.sh
```

Ou manuellement :

```bash
pip3 install --user -r requirements.txt
```

### 3. Lancer l'application

```bash
python3 video_organizer.py
```

Ou directement :

```bash
./video_organizer.py
```

## Premier usage

1. **Configurer les dossiers** :
   - Cliquez sur "📁 Sélectionner dossier source"
   - Choisissez le dossier contenant vos vidéos
   - Cliquez sur "📂 Dossier de destination"
   - Choisissez où vous voulez organiser vos vidéos

2. **Organiser une vidéo** :
   - Attendez que les miniatures se chargent
   - Cochez les tags appropriés (ex: indoor, bathroom, bikini)
   - Cliquez sur "✓ Valider"
   - La vidéo sera déplacée dans : `destination/bathroom/bikini/indoor/`

3. **Ajouter des tags** :
   - Cliquez sur "+ Tag" sous une vidéo
   - Entrez le nom du nouveau tag
   - Il sera disponible pour toutes les vidéos

## Tags par défaut

L'application est livrée avec ces tags :
- indoor
- outdoor
- bathroom
- bedroom
- kitchen
- bikini
- bdsm
- rooftop
- pool
- gym

Vous pouvez en ajouter autant que vous voulez !

## Organisation des fichiers

Les vidéos sont organisées ainsi :

```
Dossier de destination/
├── indoor/
│   ├── bathroom/
│   │   └── bikini/
│   │       └── video1.mp4
│   └── bedroom/
│       └── lingerie/
│           └── video2.mp4
└── outdoor/
    └── rooftop/
        └── bdsm/
            └── video3.mp4
```

Les tags sont triés **alphabétiquement** dans le chemin pour éviter les doublons.

## Astuces

- **Top 10 tags** : Les 10 tags les plus utilisés apparaissent en premier dans la liste
- **Cache miniatures** : Les miniatures sont mises en cache dans `~/.cache/video_organizer/`
- **Multi-dossiers** : Vous pouvez ajouter plusieurs dossiers sources
- **Formats supportés** : MP4, AVI, MOV, MKV, WEBM, FLV, WMV, M4V
- **Rafraîchir** : Cliquez sur "🔄 Actualiser" pour recharger les vidéos

## Problèmes courants

### Les miniatures ne s'affichent pas
```bash
# Vérifiez que FFmpeg est installé
ffmpeg -version
```

### L'application ne démarre pas
```bash
# Vérifiez que PyQt6 est installé
pip3 show PyQt6

# Réinstallez si nécessaire
pip3 install --user --upgrade PyQt6
```

### Erreur "Permission denied"
```bash
# Rendez le script exécutable
chmod +x video_organizer.py
```

## Support

Pour plus d'informations, consultez `README_VIDEO_ORGANIZER.md`
