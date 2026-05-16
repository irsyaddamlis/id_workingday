# Indonesian Working Day
This library functions to provide an effective Indonesian business day calendar.

## For Install
```bash
pip install git+https://github.com/irsyad.damlis/id_workingday.git
```

## For Update
```bash
pip uninstall -y id_workingday && pip install --no-cache-dir git+https://github.com/irsyaddamlis/id_workingday.git
```

## How to Use it?

###
import id_workingday as idw

####
Table Data Effective Working Data

df = idw.working_date(start='YYYYMMDD',end='YYYYMMDD',type=int(0/1),new_year=int, ied_fitr=int,christmas=int)

* explain:

start = start date, you also can use this format 'YYYY-MM-DD'
end = end date, you also can use this format 'YYYY-MM-DD'
type 0 = is a format for working business days 'Mon, Tue, Wed, Thu, Fri, Sat'
type 1 = is a format for working business days 'Mon, Tue, Wed, Thu, Fri'
new_year/ied_fitr/christmas is additional holiday for special event new year, ied fitr and christmas