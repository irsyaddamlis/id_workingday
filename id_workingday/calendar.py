# %%
import holidays
import pandas as pd
import numpy as np
from pandas.tseries.offsets import CustomBusinessDay


def working_date(
    start: str,
    end: str,
    type: int = None,
    ied_fitr: int = 3,
    christmas: int = None,
    new_year: int = None
):
    """
    Get Indonesian working days (Mon–Sat by default, Mon-Fri if type=1) between start and end,
    excluding national + extended holidays.

    Parameters
    ----------
    start : str or datetime-like
        Start date (e.g. '2024-01-01')
    end : str or datetime-like
        End date (e.g. '2027-12-31')
    type : int, default None
        Work week type: None or 0 = Mon-Sat, 1 = Mon-Fri
    ied_fitr : int, default 3
        Number of days to extend Idul Fitri holiday.
    christmas : int, default None
        Number of days to extend Christmas holiday.
    new_year : int, default None
        Number of days to extend New Year holiday.

    Returns
    -------
    pandas.DataFrame
        DataFrame with column 'Working Date' containing all working days in the range.
    """

    # base holidays (official) from "holidays" lib
    holiday = pd.DataFrame(
        sorted(holidays.country_holidays("ID", years=pd.date_range(start=start, end=end).year).items()),
        columns=["date", "name"],
    )

    holiday["date"] = pd.to_datetime(holiday["date"])
    seasonal_event = holiday.loc[
        (holiday["name"] == "Hari kedua dari Hari Raya Idul Fitri (perkiraan)")
        | (holiday["name"].str.contains("Hari Raya Natal", case=False, na=False))
        | (holiday["name"].str.contains("Tahun Baru Masehi", case=False, na=False))
    ]

    additional_holiday = []

    for index, row in seasonal_event.iterrows():
        # FIX 1: Changed 'ied_fitri' to 'Fitri' to match holiday name
        if row['name'] == 'Hari kedua dari Hari Raya Idul Fitri (perkiraan)':
            if ied_fitr is None:
                continue
            date_range = pd.date_range(start=row['date'], periods=ied_fitr, freq='D')
        elif row['name'] == 'Hari Raya Natal':
            if christmas is None:
                continue
            date_range = pd.date_range(start=row['date'], periods=christmas, freq='D')
        else:
            if new_year is None:
                continue
            date_range = pd.date_range(start=row['date'], periods=new_year, freq='D')
        
        for holiday_dates in date_range:
            additional_holiday.append({
                'date': holiday_dates,
                'name': f"extend {row['name']}"
            })

    additional_holiday = pd.DataFrame(additional_holiday, columns=['date', 'name'])
    holiday['date'] = pd.to_datetime(holiday['date'])
    additional_holiday['date'] = pd.to_datetime(additional_holiday['date'])
    holiday = pd.concat([holiday, additional_holiday], ignore_index=True).sort_values('date').reset_index(drop=True)

    # Mon–Sat as working days (Sunday off)
    workday_type = 'Mon Tue Wed Thu Fri Sat' if type is None or type == 0 else 'Mon Tue Wed Thu Fri'
    cbd = CustomBusinessDay(
        weekmask=workday_type,
        holidays=list(holiday["date"]),
    )

    # FIX 2: Return DataFrame instead of DatetimeIndex
    wd = pd.DataFrame({'Working Date': pd.date_range(start=start, end=end, freq=cbd)})
    return wd


def total_working_day(
    start: str,
    end: str,
    type: int = None,
    ied_fitr: int = 3,
    christmas: int = None,
    new_year: int = None
):
    """
    Just returns the count of working days.
    """
    return working_date(
        start=start,
        end=end,
        type=type,
        ied_fitr=ied_fitr,
        christmas=christmas,
        new_year=new_year
    ).size


def working_day(
    start: str,
    end: str,
    type: int = None,
    ied_fitr: int = 3,
    christmas: int = None,
    new_year: int = None
):
    """
    Returns monthly breakdown of working days.
    """
    wd = working_date(
        start=start,
        end=end,
        type=type,
        ied_fitr=ied_fitr,
        christmas=christmas,
        new_year=new_year
    )
    wd['Year-Month'] = wd['Working Date'].dt.to_period('M')
    # Count working days per month
    monthly_count = wd.groupby('Year-Month').size().reset_index(name='Working Days')
    return monthly_count