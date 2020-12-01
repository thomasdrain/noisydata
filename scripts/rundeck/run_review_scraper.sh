cd /home/ubuntu/noisydata
. venv/bin/activate
cd scripts/
python3 -m data_collection.review_scraper
deactivate
cd /home/ubuntu