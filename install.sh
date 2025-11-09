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

# Check for Qt system libraries
echo ""
echo "Vérification des bibliothèques Qt système..."

MISSING_LIBS=()

# Check for xcb-cursor (required for Qt)
if ! ldconfig -p | grep -q libxcb-cursor.so; then
    MISSING_LIBS+=("libxcb-cursor0")
fi

if [ ${#MISSING_LIBS[@]} -gt 0 ]; then
    echo "⚠️  Bibliothèques Qt manquantes détectées."
    echo ""
    echo "Pour installer les dépendances Qt nécessaires:"
    echo "  sudo apt install libxcb-cursor0 libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxkbcommon-x11-0"
    echo ""
    read -p "Voulez-vous installer ces dépendances maintenant ? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt install -y libxcb-cursor0 libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxkbcommon-x11-0
        if [ $? -eq 0 ]; then
            echo "✓ Bibliothèques Qt installées"
        else
            echo "❌ Erreur lors de l'installation des bibliothèques Qt"
            echo "Vous devrez les installer manuellement pour que l'application fonctionne."
        fi
    fi
else
    echo "✓ Bibliothèques Qt trouvées"
fi

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
