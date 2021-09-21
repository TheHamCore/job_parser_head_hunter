# Parser Head_hunter
### Description
#### Service for an employee looking for a job, which allows you to receive vacancies from the head_hunter website

### Installation

#### Install the dependencies and start the server.
```
git clone https://github.com/TheHamCore/job_parser_head_hunter.git
cd scraping_service
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```

#### Update information
```
open folder "scraping" and run the file "parsers.py"
```

#### If you want to launch with a local database you will have to write next command
```python manage.py migrate```

#### Run the server
```
python manage.py runserver
```

***Check your 127.0.0.1:8000***