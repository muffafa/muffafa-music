VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

.PHONY: venv install run build-installer install-and-build clean help

# Create virtual environment
venv:
	python3 -m venv $(VENV_DIR)

# Install dependencies
install: venv
	$(PIP) install -r requirements.txt

# Run the modern tkinter application
run:
	$(PYTHON) modern_app.py

# Build installer for current platform
build-installer:
	$(PYTHON) build_installers.py

# Install dependencies and build installer
install-and-build: install
	$(PYTHON) build_installers.py

# Clean build artifacts and cache
clean:
	rm -rf $(VENV_DIR) __pycache__ *.pyc build dist *.dmg *.exe LICENSE.txt

# Show help information
help:
	@echo "🎵 Modern Audio Converter - Available Commands:"
	@echo ""
	@echo "  make install           - Install dependencies in virtual environment"
	@echo "  make run              - Run the modern tkinter application"
	@echo "  make build-installer  - Build installer for current platform"
	@echo "  make install-and-build - Install dependencies and build installer"
	@echo "  make clean            - Clean build artifacts and virtual environment"
	@echo "  make help             - Show this help message"
	@echo ""
	@echo "📦 Output: Installer files (.dmg for macOS, .exe for Windows)"
	@echo "🔧 Requirements: Python 3.7+ and make"
