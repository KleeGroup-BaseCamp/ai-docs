# Create virtualenv
virtualenv ./env --python=python3.9

# Install python requirements
pip install -r requirements.txt

# Install ghostscript
## Windows
wget https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs9540/gs9540w64.exe

## Debian
apt-get update && apt-get install -y ghostscript

# Install ocrmypdf 
## with Conda
conda install ocrmypdf

## with Windows
wget https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210811.exe

## with Debian
pip3 install ocrmypdf
apt-get install -y tesseract-ocr

# Executing database migrations
python manage.py makemigrations
python manage.py migrate

# Launch the serveur
python manage.py runserver

