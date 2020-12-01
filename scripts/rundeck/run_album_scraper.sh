cd /home/ubuntu/noisydata
. venv/bin/activate
cd scripts/
python3 -m data_collection.album_scraper
deactivate
cd /home/ubuntu