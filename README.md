# data-storages-app
Project for Data Storages Course

# TODO

remove script.py


## Install
Create environment
```
python -m venv .venv
source .venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

Configure the Enviroment variables. For development stage, you can use an .env file:

```
cp .env.example .env
```

then fill each variable with its true value ;)

## Models
Create a model class in some file within the folder models like this:

```python
from manager.models_type import *

@table_keys('PublisherId')
class Publisher:
    PublisherId = DBInt(autogenerated=True)
    Name = DBVarchar()
```

## Development Information

We provide some dummy data to fill the tables. They are located in the folder data as json files. Each file name match the model class in the model folder.

Some of the dummy data its generated randomly and it is not included in the data folder.