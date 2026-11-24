from datetime import datetime
from models import TrackerItem
from validators import required, validate_priority, validate_due_date, validate_status
import storage

class ProjectTracker:
    def __init__(self):
        self.items = storage.load_items()
        self.counters = {"RFI": 0, "DEF": 0}
        for item_id in self.items:
            prefix = item_id.split("-")[0]
            if prefix in self.counters:
                try:
                    self.counters[prefix] = max(self.counters[prefix], int(item_id.split("-")[1]))
                except (IndexError, ValueError):
                    pass

    def _next_id(self, item_type):
        self.counters[item_type] += 1
        return f"{item_type}-{self.counters[item_type]:04d}"

    def _validate_common(self, data):
        clean = dict(data)
        for field in ("project", "location", "assigned_to"):
            clean[field] = required(clean[field], field.replace("_", " ").title())
        clean["due_date"] = validate_due_date(clean["due_date"])
        clean["priority"] = validate_priority(clean["priority"])
        return clean

    def create_rfi(self, data):
        clean = self._validate_common(data)
        clean["subject"] = required(clean["subject"], "RFI subject")
        clean["question"] = required(clean["question"], "Technical question")
        item_id = self._next_id("RFI")
        self.items[item_id] = TrackerItem.new(item_id, "RFI", clean).to_dict()
        storage.save_items(self.items)
        return item_id

    def create_deficiency(self, data):
        clean = self._validate_common(data)
        clean["title"] = required(clean["title"], "Deficiency title")
        clean["description"] = required(clean["description"], "Deficiency description")
        clean["trade"] = required(clean["trade"], "Responsible trade")
        item_id = self._next_id("DEF")
        self.items[item_id] = TrackerItem.new(item_id, "DEF", clean).to_dict()
        storage.save_items(self.items)
        return item_id

    def update_status(self, item_type, item_id, status, note=""):
        item_type = item_type.upper()
        if item_type not in {"RFI", "DEF"}:
            raise ValueError("Item type must be RFI or DEF.")
        if item_id not in self.items:
            raise KeyError(f"{item_id} was not found.")
        item = self.items[item_id]
        if item["item_type"] != item_type:
            raise ValueError(f"{item_id} is not a {item_type}.")
        new_status = validate_status(item_type, status)
        now = datetime.now().isoformat(timespec="seconds")
        item["status"] = new_status
        item["updated_at"] = now
        item.setdefault("history", []).append({
            "timestamp": now,
            "status": new_status,
            "note": str(note).strip()
        })
        storage.save_items(self.items)

    def overdue_items(self):
        today = datetime.now().date()
        result = []
        for item in self.items.values():
            if item["status"] == "CLOSED" or item["due_date"].upper() == "N/A":
                continue
            due = datetime.strptime(item["due_date"], "%Y-%m-%d").date()
            if due < today:
                result.append(item)
        return result

    def open_items(self):
        return [item for item in self.items.values() if item["status"] != "CLOSED"]
