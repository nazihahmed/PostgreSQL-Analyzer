## Set-up Instructions

1. Create the news database in PostgreSQL
  - From the command line, launch the psql console by typing: psql
  - Check to see if a news database already exists by listing all databases with the command:
  ```python
   \l
   ```
   - If a news database already exists, drop it with the command: DROP DATABASE news;
   - Create the news database with the command: CREATE DATABASE news;
   - exit the console by typing: \q
2. From the command line, navigate to the directory containing newsdata.sql.
3. Import the schema and data in newsdata.sql to the news database by typing:
```python
psql -d news -f newsdata.sql
```

## How to run

1. Once the news database has been set up, from the command line navigate to the directory containing analyzer.py.
2. Run the script by typing:
```python
python analyzer.py
 ```
![Example of running the program](/example of running the program.PNG?raw=true)
