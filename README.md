# crumbl-cookie-predictor
for fun project incorporating NLP, sequence prediction, and software engineering

# Quickstart
```
python (or python3) -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:/your/filepath/to/this/repo/crumbl-cookie-predictor"
```
# TODO - Data Scraping
- Currently, the implementation for chromedriver within the `all_cookie_occurances_scraper.py` doesn't have a "catch-all" script implemented, that could be a challenge for later (like adding a bash script that automatically downloads it for you?)
- Finish `all_cookie_occurances_scraper.py` script so it populates a sqlite database 
- Finish `database.py` so that we can have it output a pandas dataframe containing data for any sqlite database it ingests

# TODO - Analysis
- I need to write this section

# TODO - UI 
- I need to write this section (this will be a React TSX App though [for practice])

# TODO - ML
- We also need to see if we can find a metric of cookie popularity out there? Scrape instagram? not sure.
- I don't even know if this is going to work but whatever:
    - Naive Logistic Model preciting "Will a Cookie Come out this week"
    - Neural Network with cookie embedded as IDs
    - some sort of RNN to develop
    - Cookie Vectors based on their names
    - GAN based on cookie vectors
    - GAN based on just cookies
    - Predictor for Name of new cookie coming out next week
    - Neural Network which tries to predict the likely hood of cookie return

# TODO - AWS
- Set up AWS CDK for S3 Buckets
- Set up Pipeline for development

# TODO - DEVOPS
- Docker?
- Circle CI?
- Linting?
- Unittests?
- Logging?
