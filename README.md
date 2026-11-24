# RFI & Construction Deficiency Tracker

A small Python command-line application to register and monitor Requests for Information
(RFIs) and construction deficiencies in a project.

## Features
- Create RFIs with technical questions, drawing/specification references, location,
  assigned reviewer, priority, and response due date.
- Record construction deficiencies with description, trade, location, responsible party,
  corrective due date, and drawing/specification reference.
- Update statuses and retain a dated status/comment history.
- View separate RFI and deficiency registers.
- Identify open and overdue items.
- Export RFI and deficiency registers to separate CSV files.
- Persist data locally in a JSON file.

## Project files
- `main.py` — interactive command-line menu.
- `models.py` — common tracker item data model.
- `validators.py` — validates priorities, dates, and statuses.
- `tracker.py` — creates items, updates statuses, and checks overdue items.
- `storage.py` — saves and loads records.
- `reports.py` — displays registers and exports CSV reports.

## Requirements
Python 3.9 or newer. Uses only the Python standard library.

## Run
```bash
python main.py
```

The application creates `data/tracker_items.json` to store records and a `reports/`
folder when CSV exports are generated.

## Status options
**RFI:** OPEN, PENDING RESPONSE, ANSWERED, CLOSED

**Deficiency:** OPEN, ASSIGNED, IN PROGRESS, READY FOR REINSPECTION, CLOSED

## Important note
This is a basic tracking and documentation aid. It does not replace the project's
formal RFI workflow, contract requirements, approved submittal process, inspection
procedures, or documented acceptance by the responsible design professional or owner.
