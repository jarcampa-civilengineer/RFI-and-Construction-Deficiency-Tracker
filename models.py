from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class TrackerItem:
    item_id: str
    item_type: str
    project: str
    title: str
    description: str
    location: str
    assigned_to: str
    due_date: str
    priority: str
    status: str
    created_at: str
    updated_at: str
    references: str = ""
    submitted_by: str = ""
    trade: str = ""
    history: list = None

    def to_dict(self):
        result = asdict(self)
        result["history"] = self.history or []
        return result

    @classmethod
    def new(cls, item_id, item_type, data):
        now = datetime.now().isoformat(timespec="seconds")
        if item_type == "RFI":
            title = data["subject"]
            description = data["question"]
            references = data.get("spec_section", "N/A")
            submitted_by = data.get("submitted_by", "")
            trade = ""
            initial_status = "OPEN"
        else:
            title = data["title"]
            description = data["description"]
            references = data.get("drawing_spec", "N/A")
            submitted_by = data.get("reported_by", "")
            trade = data.get("trade", "")
            initial_status = "OPEN"
        return cls(
            item_id=item_id,
            item_type=item_type,
            project=data["project"],
            title=title,
            description=description,
            location=data["location"],
            assigned_to=data["assigned_to"],
            due_date=data["due_date"],
            priority=data["priority"].upper(),
            status=initial_status,
            created_at=now,
            updated_at=now,
            references=references,
            submitted_by=submitted_by,
            trade=trade,
            history=[{"timestamp": now, "status": initial_status, "note": "Item created"}],
        )
