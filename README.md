# How to gather data from https://rammount.com?

## Install Python
https://www.python.org/downloads/


## Virtual environment
It's strongly reccomended to activate virtual environment

https://docs.python.org/3/library/venv.html


## Install requirements
```shell
pip install -r requirements.txt 
```

## Run script
```shell
python process_rammount_com_data.py 
```

## Observe results
There should be two (2) files:
* `products.csv`
* `collections.csv`


# Excel file for reference

Check `products-collections.xlsx` - it contains already loaded `products` and `collections`.

If you want to load your data, you have to change paths in Power Query editor to files:
* `\\wsl.localhost\Ubuntu\home\psz\dev\_tmp\michal\products.csv`
* `\\wsl.localhost\Ubuntu\home\psz\dev\_tmp\michal\collections.csv`
