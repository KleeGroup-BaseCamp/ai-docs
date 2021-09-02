
# Create virtualenv
virtualenv ./env --python=python3.9

# Install python requirements
pip install -r requirments.txt

# Install ghostscript
wget https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs9540/gs9540w64.exe

# Install ocrmypdf 
## with Conda
conda install ocrmypdf

## with Windows
wget https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210811.exe

# Executing database migrations
python manage.py makemigrations
python manage.py migrate

# Launch the serveur
python manage.py runserver

