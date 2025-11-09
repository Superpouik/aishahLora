#!/usr/bin/env python3
"""
Video Organizer - Organize AI-generated videos with tags
"""

import sys
import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QGridLayout, QFileDialog,
    QDialog, QLineEdit, QListWidget, QMessageBox, QFrame, QCheckBox,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage


class Config:
    """Manage application configuration"""

    def __init__(self, config_path: str = "video_organizer_config.json"):
        self.config_path = config_path
        self.data = self.load()

    def load(self) -> Dict:
        """Load configuration from file"""
        default_config = {
            "tags": ["indoor", "outdoor", "bathroom", "bedroom", "kitchen",
                    "bikini", "bdsm", "rooftop", "pool", "gym"],
            "tag_usage": {},
            "source_folders": [],
            "destination_folder": "",
            "thumbnail_cache": {}
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except Exception as e:
                print(f"Error loading config: {e}")

        return default_config

    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_sorted_tags(self) -> List[str]:
        """Get tags sorted by usage (top 10) then alphabetically"""
        tags = self.data.get("tags", [])
        usage = self.data.get("tag_usage", {})

        # Sort by usage count (descending)
        sorted_by_usage = sorted(tags, key=lambda t: usage.get(t, 0), reverse=True)

        # Top 10 most used
        top_tags = sorted_by_usage[:10]

        # Remaining tags sorted alphabetically
        remaining_tags = sorted([t for t in tags if t not in top_tags])

        return top_tags + remaining_tags

    def increment_tag_usage(self, tag: str):
        """Increment usage count for a tag"""
        if "tag_usage" not in self.data:
            self.data["tag_usage"] = {}

        self.data["tag_usage"][tag] = self.data["tag_usage"].get(tag, 0) + 1
        self.save()

    def add_tag(self, tag: str):
        """Add a new tag"""
        if "tags" not in self.data:
            self.data["tags"] = []

        if tag not in self.data["tags"]:
            self.data["tags"].append(tag)
            self.save()
            return True
        return False


class ThumbnailGenerator(QThread):
    """Generate video thumbnails in background"""

    thumbnail_ready = pyqtSignal(str, str)  # video_path, thumbnail_path

    def __init__(self, video_path: str, thumbnail_path: str):
        super().__init__()
        self.video_path = video_path
        self.thumbnail_path = thumbnail_path

    def run(self):
        """Generate thumbnail using ffmpeg"""
        try:
            # Create thumbnail directory if it doesn't exist
            os.makedirs(os.path.dirname(self.thumbnail_path), exist_ok=True)

            # Use ffmpeg to extract frame at 1 second
            cmd = [
                'ffmpeg',
                '-i', self.video_path,
                '-ss', '00:00:01',
                '-vframes', '1',
                '-vf', 'scale=320:180:force_original_aspect_ratio=decrease',
                '-y',
                self.thumbnail_path
            ]

            subprocess.run(cmd, capture_output=True, check=True)
            self.thumbnail_ready.emit(self.video_path, self.thumbnail_path)
        except Exception as e:
            print(f"Error generating thumbnail for {self.video_path}: {e}")
            self.thumbnail_ready.emit(self.video_path, "")


class VideoCard(QFrame):
    """Widget representing a single video with tags"""

    def __init__(self, video_path: str, config: Config, parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.config = config
        self.selected_tags = set()

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        self.setMaximumWidth(350)

        self.setup_ui()

    def setup_ui(self):
        """Setup the card UI"""
        layout = QVBoxLayout()

        # Thumbnail
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(320, 180)
        self.thumbnail_label.setStyleSheet("background-color: #2b2b2b; color: white;")
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setText("Chargement...")
        layout.addWidget(self.thumbnail_label)

        # Video name
        video_name = os.path.basename(self.video_path)
        name_label = QLabel(video_name)
        name_label.setWordWrap(True)
        name_label.setMaximumWidth(320)
        name_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(name_label)

        # Tags scroll area
        tags_scroll = QScrollArea()
        tags_scroll.setWidgetResizable(True)
        tags_scroll.setMaximumHeight(120)

        tags_widget = QWidget()
        self.tags_layout = QVBoxLayout(tags_widget)
        self.tags_layout.setSpacing(2)

        # Create tag checkboxes
        self.tag_checkboxes = {}
        for tag in self.config.get_sorted_tags():
            cb = QCheckBox(tag)
            cb.stateChanged.connect(self.on_tag_changed)
            self.tag_checkboxes[tag] = cb
            self.tags_layout.addWidget(cb)

        tags_scroll.setWidget(tags_widget)
        layout.addWidget(tags_scroll)

        # Bottom buttons
        button_layout = QHBoxLayout()

        # Add tag button
        add_tag_btn = QPushButton("+ Tag")
        add_tag_btn.clicked.connect(self.add_new_tag)
        button_layout.addWidget(add_tag_btn)

        # Validate button
        self.validate_btn = QPushButton("✓ Valider")
        self.validate_btn.setEnabled(False)
        self.validate_btn.setStyleSheet("""
            QPushButton:enabled {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
        """)
        self.validate_btn.clicked.connect(self.validate)
        button_layout.addWidget(self.validate_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Generate thumbnail
        self.generate_thumbnail()

    def generate_thumbnail(self):
        """Generate and display thumbnail"""
        # Check cache first
        cache = self.config.data.get("thumbnail_cache", {})
        if self.video_path in cache and os.path.exists(cache[self.video_path]):
            self.set_thumbnail(cache[self.video_path])
            return

        # Generate new thumbnail
        thumbnail_dir = os.path.expanduser("~/.cache/video_organizer/thumbnails")
        os.makedirs(thumbnail_dir, exist_ok=True)

        video_hash = str(hash(self.video_path))
        thumbnail_path = os.path.join(thumbnail_dir, f"{video_hash}.jpg")

        self.thumbnail_thread = ThumbnailGenerator(self.video_path, thumbnail_path)
        self.thumbnail_thread.thumbnail_ready.connect(self.on_thumbnail_ready)
        self.thumbnail_thread.start()

    def on_thumbnail_ready(self, video_path: str, thumbnail_path: str):
        """Callback when thumbnail is ready"""
        if video_path == self.video_path and thumbnail_path and os.path.exists(thumbnail_path):
            # Update cache
            if "thumbnail_cache" not in self.config.data:
                self.config.data["thumbnail_cache"] = {}
            self.config.data["thumbnail_cache"][video_path] = thumbnail_path
            self.config.save()

            self.set_thumbnail(thumbnail_path)

    def set_thumbnail(self, thumbnail_path: str):
        """Set the thumbnail image"""
        pixmap = QPixmap(thumbnail_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                320, 180,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.thumbnail_label.setPixmap(scaled_pixmap)
        else:
            self.thumbnail_label.setText("Erreur")

    def on_tag_changed(self):
        """Handle tag checkbox state change"""
        self.selected_tags = {
            tag for tag, cb in self.tag_checkboxes.items() if cb.isChecked()
        }
        self.validate_btn.setEnabled(len(self.selected_tags) > 0)

    def add_new_tag(self):
        """Show dialog to add new tag"""
        dialog = AddTagDialog(self.config, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Refresh tag list
            self.refresh_tags()

    def refresh_tags(self):
        """Refresh the tag list"""
        # Clear existing checkboxes
        for cb in self.tag_checkboxes.values():
            self.tags_layout.removeWidget(cb)
            cb.deleteLater()

        self.tag_checkboxes.clear()

        # Recreate checkboxes
        for tag in self.config.get_sorted_tags():
            cb = QCheckBox(tag)
            cb.stateChanged.connect(self.on_tag_changed)
            if tag in self.selected_tags:
                cb.setChecked(True)
            self.tag_checkboxes[tag] = cb
            self.tags_layout.addWidget(cb)

    def validate(self):
        """Validate and move video to organized location"""
        if not self.selected_tags:
            return

        destination_base = self.config.data.get("destination_folder", "")
        if not destination_base or not os.path.exists(destination_base):
            QMessageBox.warning(
                self,
                "Erreur",
                "Le dossier de destination n'est pas configuré ou n'existe pas."
            )
            return

        # Create subdirectory path from tags
        tag_path = os.path.join(destination_base, *sorted(self.selected_tags))

        try:
            # Create directory structure
            os.makedirs(tag_path, exist_ok=True)

            # Move video
            video_name = os.path.basename(self.video_path)
            destination = os.path.join(tag_path, video_name)

            # Handle duplicate names
            if os.path.exists(destination):
                base, ext = os.path.splitext(video_name)
                counter = 1
                while os.path.exists(destination):
                    new_name = f"{base}_{counter}{ext}"
                    destination = os.path.join(tag_path, new_name)
                    counter += 1

            shutil.move(self.video_path, destination)

            # Update tag usage statistics
            for tag in self.selected_tags:
                self.config.increment_tag_usage(tag)

            # Remove this card
            self.setParent(None)
            self.deleteLater()

            QMessageBox.information(
                self,
                "Succès",
                f"Vidéo déplacée vers:\n{tag_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors du déplacement de la vidéo:\n{str(e)}"
            )


class AddTagDialog(QDialog):
    """Dialog for adding a new tag"""

    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("Ajouter un tag")
        self.setup_ui()

    def setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nouveau tag:"))

        self.tag_input = QLineEdit()
        self.tag_input.returnPressed.connect(self.accept)
        layout.addWidget(self.tag_input)

        button_layout = QHBoxLayout()

        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("Ajouter")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        """Handle accept"""
        tag = self.tag_input.text().strip()
        if tag:
            if self.config.add_tag(tag):
                super().accept()
            else:
                QMessageBox.warning(self, "Erreur", "Ce tag existe déjà.")
        else:
            QMessageBox.warning(self, "Erreur", "Le tag ne peut pas être vide.")


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.config = Config()
        self.video_cards = []

        self.setWindowTitle("Video Organizer")
        self.setMinimumSize(1200, 800)

        self.setup_ui()

        # Load saved folders if any
        if self.config.data.get("source_folders"):
            self.load_videos()

    def setup_ui(self):
        """Setup main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Top controls
        controls_layout = QHBoxLayout()

        # Source folder button
        source_btn = QPushButton("📁 Sélectionner dossier source")
        source_btn.clicked.connect(self.select_source_folder)
        controls_layout.addWidget(source_btn)

        # Destination folder button
        dest_btn = QPushButton("📂 Dossier de destination")
        dest_btn.clicked.connect(self.select_destination_folder)
        controls_layout.addWidget(dest_btn)

        # Refresh button
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.clicked.connect(self.load_videos)
        controls_layout.addWidget(refresh_btn)

        controls_layout.addStretch()

        main_layout.addLayout(controls_layout)

        # Current folders display
        self.folders_label = QLabel()
        self.update_folders_label()
        main_layout.addWidget(self.folders_label)

        # Scroll area for video grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(scroll_area)

    def update_folders_label(self):
        """Update the folders display label"""
        source_folders = self.config.data.get("source_folders", [])
        dest_folder = self.config.data.get("destination_folder", "Non défini")

        source_text = ", ".join(source_folders) if source_folders else "Non défini"

        text = f"<b>Sources:</b> {source_text}<br><b>Destination:</b> {dest_folder}"
        self.folders_label.setText(text)

    def select_source_folder(self):
        """Select source folder containing videos"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner un dossier contenant des vidéos"
        )

        if folder:
            if "source_folders" not in self.config.data:
                self.config.data["source_folders"] = []

            if folder not in self.config.data["source_folders"]:
                self.config.data["source_folders"].append(folder)
                self.config.save()

            self.update_folders_label()
            self.load_videos()

    def select_destination_folder(self):
        """Select destination folder for organized videos"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le dossier de destination"
        )

        if folder:
            self.config.data["destination_folder"] = folder
            self.config.save()
            self.update_folders_label()

    def load_videos(self):
        """Load videos from source folders"""
        # Clear existing cards
        for card in self.video_cards:
            card.setParent(None)
            card.deleteLater()
        self.video_cards.clear()

        # Get all videos
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v'}
        videos = []

        source_folders = self.config.data.get("source_folders", [])
        for folder in source_folders:
            if not os.path.exists(folder):
                continue

            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in video_extensions):
                        video_path = os.path.join(root, file)
                        mtime = os.path.getmtime(video_path)
                        videos.append((video_path, mtime))

        # Sort by modification time (newest first)
        videos.sort(key=lambda x: x[1], reverse=True)

        # Create video cards in grid
        columns = 3
        for idx, (video_path, _) in enumerate(videos):
            row = idx // columns
            col = idx % columns

            card = VideoCard(video_path, self.config, self)
            self.grid_layout.addWidget(card, row, col)
            self.video_cards.append(card)

        if not videos:
            label = QLabel("Aucune vidéo trouvée. Sélectionnez un dossier source.")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 16px; color: gray;")
            self.grid_layout.addWidget(label, 0, 0, 1, columns)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)

    # Set dark theme
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
