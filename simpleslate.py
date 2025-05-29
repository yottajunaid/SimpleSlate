import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QAction,
                             QFileDialog, QMessageBox, QFontDialog, QColorDialog,
                             QLabel, QStatusBar)
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
import base64
from io import BytesIO

# Convert your icon to base64 string (use online converter)
ICON_DATA = """
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
"""  # Replace with your actual base64 icon data


class SimpleSlate(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.is_dark_mode = False
        self.document_modified = False
        self.init_ui()

    def init_ui(self):
        # Create text editor widget
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Set default font
        default_font = QFont("Consolas", 11)
        self.text_edit.setFont(default_font)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Ready")
        self.status_bar.addPermanentWidget(self.status_label)

        # Text changed connection
        self.text_edit.textChanged.connect(self.text_changed)

        # Create menu bar actions
        self.create_file_menu()
        self.create_edit_menu()
        self.create_format_menu()
        self.create_view_menu()
        self.create_help_menu()

        # Set window properties
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("SimpleSlate")
        self.apply_light_theme()  # Set default theme
        self.show()

        # Set application icon (add this after self.text_edit = QTextEdit())
        try:
            icon_data = base64.b64decode(ICON_DATA)
            icon_pixmap = QPixmap()
            icon_pixmap.loadFromData(icon_data)
            self.setWindowIcon(QIcon(icon_pixmap))
        except Exception:
            pass

        try:
            # Try to load icon from the same directory as the executable
            icon_path = os.path.join(os.path.dirname(sys.argv[0]), "icon.ico")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
            else:
                # Fallback: try loading from current directory
                if os.path.exists("icon.ico"):
                    self.setWindowIcon(QIcon("icon.ico"))
        except Exception:
            pass  # If icon loading fails, continue without icon

    def create_file_menu(self):
        # File menu
        file_menu = self.menuBar().addMenu("File")

        # New action
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        # Open action
        open_action = QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Save action
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Save As action
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        # Print action
        print_action = QAction("Print...", self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_document)
        file_menu.addAction(print_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_edit_menu(self):
        # Edit menu
        edit_menu = self.menuBar().addMenu("Edit")

        # Undo action
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        # Redo action
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        # Cut action
        cut_action = QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        # Copy action
        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        # Paste action
        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        # Delete action
        delete_action = QAction("Delete", self)
        delete_action.setShortcut("Del")
        delete_action.triggered.connect(lambda: self.text_edit.textCursor().removeSelectedText())
        edit_menu.addAction(delete_action)

        edit_menu.addSeparator()

        # Select All action
        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)

        # Find action
        find_action = QAction("Find...", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.find_text)
        edit_menu.addAction(find_action)

        # Time/Date action
        time_date_action = QAction("Time/Date", self)
        time_date_action.setShortcut("F5")
        time_date_action.triggered.connect(self.insert_datetime)
        edit_menu.addAction(time_date_action)

    def create_format_menu(self):
        # Format menu
        format_menu = self.menuBar().addMenu("Format")

        # Word Wrap action
        word_wrap_action = QAction("Word Wrap", self)
        word_wrap_action.setCheckable(True)
        word_wrap_action.setChecked(True)
        word_wrap_action.triggered.connect(self.toggle_word_wrap)
        format_menu.addAction(word_wrap_action)

        # Font action
        font_action = QAction("Font...", self)
        font_action.triggered.connect(self.choose_font)
        format_menu.addAction(font_action)

        # Color action
        color_action = QAction("Text Color...", self)
        color_action.triggered.connect(self.choose_color)
        format_menu.addAction(color_action)

    def create_view_menu(self):
        # View menu
        view_menu = self.menuBar().addMenu("View")

        # Light/Dark Mode toggle
        theme_action = QAction("Dark Mode", self)
        theme_action.setCheckable(True)
        theme_action.setChecked(False)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        self.theme_action = theme_action  # Store reference for later updates

        view_menu.addSeparator()

        # Background Color action
        bg_color_action = QAction("Background Color...", self)
        bg_color_action.triggered.connect(self.choose_background_color)
        view_menu.addAction(bg_color_action)

        view_menu.addSeparator()

        # Status Bar action
        status_bar_action = QAction("Status Bar", self)
        status_bar_action.setCheckable(True)
        status_bar_action.setChecked(True)
        status_bar_action.triggered.connect(self.toggle_status_bar)
        view_menu.addAction(status_bar_action)

    def create_help_menu(self):
        # Help menu
        help_menu = self.menuBar().addMenu("Help")

        # About action
        about_action = QAction("About SimpleSlate", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def new_file(self):
        if self.maybe_save():
            self.text_edit.clear()
            self.current_file = None
            self.document_modified = False
            self.setWindowTitle("SimpleSlate")
            self.status_label.setText("New file created")

    def open_file(self):
        if self.maybe_save():
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Open File", "", "Text Files (*.txt);;All Files (*)"
            )

            if file_name:
                try:
                    with open(file_name, 'r', encoding='utf-8') as file:
                        self.text_edit.setText(file.read())

                    self.current_file = file_name
                    self.document_modified = False
                    self.setWindowTitle(f"SimpleSlate - {os.path.basename(file_name)}")
                    self.status_label.setText(f"Opened {file_name}")
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Cannot open file: {str(e)}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.text_edit.toPlainText())

                self.document_modified = False
                self.update_window_title()
                self.status_label.setText(f"Saved to {self.current_file}")
                return True
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Cannot save file: {str(e)}")
                return False
        else:
            return self.save_file_as()

    def save_file_as(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save As", "", "Text Files (*.txt);;All Files (*)"
        )

        if file_name:
            self.current_file = file_name
            self.setWindowTitle(f"SimpleSlate - {os.path.basename(file_name)}")
            return self.save_file()

        return False

    def maybe_save(self):
        if not self.document_modified:
            return True

        reply = QMessageBox.question(
            self, "SimpleSlate",
            "The document has been modified.\nDo you want to save your changes?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )

        if reply == QMessageBox.Save:
            return self.save_file()
        elif reply == QMessageBox.Cancel:
            return False

        return True

    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

    def find_text(self):
        from PyQt5.QtWidgets import QInputDialog
        from PyQt5.QtGui import QTextCursor
        # Simple find implementation
        text, ok = QInputDialog.getText(self, "Find", "Find what:")
        if ok and text:
            if not self.text_edit.find(text):
                # If not found, wrap around to beginning
                cursor = self.text_edit.textCursor()
                cursor.movePosition(QTextCursor.Start)
                self.text_edit.setTextCursor(cursor)
                if not self.text_edit.find(text):
                    QMessageBox.information(self, "Find", f"Cannot find '{text}'")

    def print_document(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.text_edit.print_(printer)
            self.status_label.setText("Document printed")

    def insert_datetime(self):
        from datetime import datetime
        self.text_edit.insertPlainText(datetime.now().strftime("%H:%M %d/%m/%Y"))

    def toggle_word_wrap(self, checked):
        if checked:
            self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        else:
            self.text_edit.setLineWrapMode(QTextEdit.NoWrap)

    def choose_font(self):
        current_font = self.text_edit.currentFont()
        font, ok = QFontDialog.getFont(current_font, self)
        if ok:
            self.text_edit.setFont(font)

    def choose_color(self):
        color = QColorDialog.getColor(self.text_edit.textColor(), self)
        if color.isValid():
            self.text_edit.setTextColor(color)

    def toggle_status_bar(self, checked):
        self.statusBar().setVisible(checked)

    def text_changed(self):
        # Update document modified state
        self.document_modified = True
        self.update_window_title()

        # Update status bar with character and word count
        text = self.text_edit.toPlainText()
        char_count = len(text)
        word_count = len(text.split()) if text else 0

        self.status_label.setText(f"Characters: {char_count} | Words: {word_count}")

    def update_window_title(self):
        if self.current_file:
            filename = os.path.basename(self.current_file)
            if self.document_modified:
                self.setWindowTitle(f"*SimpleSlate - {filename}")
            else:
                self.setWindowTitle(f"SimpleSlate - {filename}")
        else:
            if self.document_modified:
                self.setWindowTitle("*SimpleSlate")
            else:
                self.setWindowTitle("SimpleSlate")

    def show_about(self):
        QMessageBox.about(
            self,
            "About SimpleSlate",
            "SimpleSlate 1.0\n\n"
            "A simple text editor made by yottajunaid\n"
            "Github: @yottajunaid\n"
        )

    def toggle_theme(self, checked):
        if checked:
            self.apply_dark_theme()
            self.theme_action.setText("Light Mode")
        else:
            self.apply_light_theme()
            self.theme_action.setText("Dark Mode")

    def apply_light_theme(self):
        self.is_dark_mode = False
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
                color: #000000;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
            }
            QMenuBar {
                background-color: #f0f0f0;
                color: #000000;
                border-bottom: 1px solid #cccccc;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 8px;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QMenu {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
            }
            QMenu::item:selected {
                background-color: #e0e0e0;
            }
            QStatusBar {
                background-color: #f0f0f0;
                color: #000000;
                border-top: 1px solid #cccccc;
            }
        """)

    def apply_dark_theme(self):
        self.is_dark_mode = True
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
                border-bottom: 1px solid #555555;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 8px;
            }
            QMenuBar::item:selected {
                background-color: #404040;
            }
            QMenu {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QMenu::item:selected {
                background-color: #404040;
            }
            QStatusBar {
                background-color: #2b2b2b;
                color: #ffffff;
                border-top: 1px solid #555555;
            }
        """)

    def choose_background_color(self):
        color = QColorDialog.getColor(self.text_edit.palette().color(self.text_edit.backgroundRole()), self)
        if color.isValid():
            # Create custom stylesheet for background color while preserving font
            current_text_color = self.text_edit.textColor().name()
            current_font = self.text_edit.font()

            self.text_edit.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {color.name()};
                    color: {current_text_color};
                    border: 1px solid #cccccc;
                }}
            """)
            # Reapply the font after stylesheet change
            self.text_edit.setFont(current_font)
            self.status_label.setText(f"Background color changed to {color.name()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = SimpleSlate()
    sys.exit(app.exec_())