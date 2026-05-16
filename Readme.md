# 🇮🇩 Indonesian Working Day

A Python library to generate Indonesian business day calendars, excluding national holidays and configurable extended holidays (Idul Fitri, Christmas, New Year).

---

## Installation

```bash
pip install git+https://github.com/irsyaddamlis/id_workingday.git
```

## Update

```bash
pip3 install --force-reinstall --user --no-cache-dir git+https://github.com/irsyaddamlis/id_workingday.git
```

---

## Quick Start

```python
import id_workingday as idw
```

---

## Functions

### 1. `working_date()` — List of Working Dates
Returns a DataFrame of all effective business working dates in the given range.

```python
df = idw.working_date(
    start='2026-01-01', # you also can use this format '20260101'
    end='2026-12-31', # you also can use this format '20260131'
    type=0,         # 0 = Mon–Sat, 1 = Mon–Fri (default 0)
    ied_fitr=3,     # extend Idul Fitri holiday by N days
    christmas=2,    # extend Christmas holiday by N days
    new_year=1      # extend New Year holiday by N days
)
```

**Output:**
| Working Date |
|---|
| 2026-01-02 |
| 2026-01-03 |
| ... |

---

### 2. `working_day()` — Monthly Working Day Count
Returns a DataFrame with the total number of working days per month.

```python
df = idw.working_day(
    start='2026-01-01',
    end='2026-12-31',
    type=0,
    ied_fitr=3,
    christmas=2,
    new_year=1
)
```

**Output:**
| Year-Month | Working Days |
|---|---|
| 2026-01 | 25 |
| 2026-02 | 24 |
| ... | ... |

---

### 3. `total_working_day()` — Total Working Day Count
Returns a single integer — the total number of working days in the range.

```python
total = idw.total_working_day(
    start='2026-01-01',
    end='2026-12-31',
    type=0,
    ied_fitr=3,
    christmas=2,
    new_year=1
)
# Output: 287
```

---

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `start` | `str` | required | Start date. Accepts `'YYYY-MM-DD'` or `'YYYYMMDD'` |
| `end` | `str` | required | End date. Accepts `'YYYY-MM-DD'` or `'YYYYMMDD'` |
| `type` | `int` | `0` | `0` = Mon–Sat, `1` = Mon–Fri |
| `ied_fitr` | `int` | `3` | Number of extra days added after Idul Fitri. Set `None` to disable |
| `christmas` | `int` | `None` | Number of extra days added after Christmas. Set `None` to disable |
| `new_year` | `int` | `None` | Number of extra days added after New Year. Set `None` to disable |

---

## Notes
- National holidays are sourced from the [`holidays`](https://github.com/vacanza/python-holidays) library.
- Extended holidays start from the official holiday date and extend forward by N days.
- Sunday is always a non-working day regardless of `type`.