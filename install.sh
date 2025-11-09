#!/bin/bash

echo "==================================="
echo "Video Organizer - Installation"
echo "==================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✓ Python 3 trouvé: $(python3 --version)"

# Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "⚠️  FFmpeg n'est pas installé."
    echo "FFmpeg est nécessaire pour générer les miniatures vidéo."
    echo ""
    echo "Pour l'installer:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  Fedora: sudo dnf install ffmpeg"
    echo "  Arch Linux: sudo pacman -S ffmpeg"
    echo ""
    read -p "Voulez-vous continuer sans FFmpeg ? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ FFmpeg trouvé: $(ffmpeg -version | head -n1)"
fi

# Install Python dependencies
echo ""
echo "Installation des dépendances Python..."
pip3 install --user -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Installation terminée avec succès!"
    echo ""
    echo "Pour lancer l'application:"
    echo "  python3 video_organizer.py"
    echo ""
    echo "Ou rendez-le exécutable:"
    echo "  chmod +x video_organizer.py"
    echo "  ./video_organizer.py"
else
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi
