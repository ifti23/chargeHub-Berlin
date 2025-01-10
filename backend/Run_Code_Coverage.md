# How to run the Code Coverage report

1. install the package

```bash
pip install coverage
```
2. run the coverage report

```bat
set PYTHONPATH=<path-to>\chargeHub-Berlin\backend && coverage run -m unittest discover
```

3. open the coverage report

```bat
coverage html
```

4. open the html report
go to the folder where the html report is saved (**htmlcov**) and open the index.html
