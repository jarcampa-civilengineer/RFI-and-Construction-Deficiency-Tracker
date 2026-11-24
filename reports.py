import csv
from pathlib import Path
from datetime import datetime

class ReportGenerator:
    def __init__(self, tracker):
        self.tracker = tracker

    def list_items(self, item_type):
        items = [i for i in self.tracker.items.values() if i["item_type"] == item_type]
        if not items:
            print(f"No {item_type} items recorded.")
            return
        print(f"\n{item_type} REGISTER")
        print("ID | PROJECT | TITLE | LOCATION | ASSIGNED TO | DUE DATE | PRIORITY | STATUS")
        print("-" * 120)
        for i in items:
            print(f"{i['item_id']} | {i['project']} | {i['title']} | {i['location']} | "
                  f"{i['assigned_to']} | {i['due_date']} | {i['priority']} | {i['status']}")

    def list_open_overdue(self):
        open_items = self.tracker.open_items()
        overdue = self.tracker.overdue_items()
        print(f"\nOpen items: {len(open_items)}")
        print(f"Overdue items: {len(overdue)}")
        for item in overdue:
            print(f"- {item['item_id']} | {item['title']} | Due {item['due_date']} | {item['status']}")

    def export_all(self):
        output_dir = Path(__file__).parent / "reports"
        output_dir.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fields = [
            "item_id", "item_type", "project", "title", "description", "location",
            "assigned_to", "due_date", "priority", "status", "created_at", "updated_at",
            "references", "submitted_by", "trade"
        ]
        paths = []
        for item_type in ("RFI", "DEF"):
            path = output_dir / f"{item_type.lower()}_register_{stamp}.csv"
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for item in self.tracker.items.values():
                    if item["item_type"] == item_type:
                        writer.writerow({key: item.get(key, "") for key in fields})
            paths.append(path)
        return paths
