## Introduction
```
'MGNREGA' is an console application for mgnrega projects and its member management
it consist of three roles:

1. Block Development Officer (Admin)
2. Gram Panchayat Member
3. Member

```
## Download

```
cd MGNREGA_HOME
git clone https://github.com/Riyazuddin489/mgnrega.git
cd MGNREGA
```


Activate your Python virtual environment, and download the required libraries
```
source venv/bin/activate
export PYTHONPATH = '.'
pip install -r requirements.txt
```

## How to run app on local laptop

Follow the guide here to ensure you run correct main file
```
python mgnrega/login.py
```

To connect to your local sqlite: 

```
MGNREGA> cd data
MGNREGA/data>  sqlite3 mgnrega.db
MGNREGA/data> select * from <your_table> (or describe <your_table>)
```

Database schema is created once via the file `data/schema_script.sql`



Key Entities in Code
----
```   
+-- common
|  +--connect_db.py
|  +--constants.py
|  +--helper.py
|  +--password_encryption.py

+-- data
|  +--mgnrega.py
|  +--schema_script.sql

+-- mgnrega
|  +--bdo.py
|  +--config.yaml
|  +--gpm.py
|  +--login.py
|  +--member.py

 
```
