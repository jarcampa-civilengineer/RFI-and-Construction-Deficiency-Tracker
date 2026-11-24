from datetime import datetime

VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}
VALID_RFI_STATUSES = {"OPEN", "PENDING RESPONSE", "ANSWERED", "CLOSED"}
VALID_DEF_STATUSES = {"OPEN", "ASSIGNED", "IN PROGRESS", "READY FOR REINSPECTION", "CLOSED"}

def required(value, label):
    value = str(value).strip()
    if not value:
        raise ValueError(f"{label} is required.")
    return value

def validate_priority(value):
    value = required(value, "Priority").upper()
    if value not in VALID_PRIORITIES:
        raise ValueError("Priority must be Low, Medium, or High.")
    return value

def validate_due_date(value):
    value = required(value, "Due date")
    if value.upper() == "N/A":
        return value
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Due date must use YYYY-MM-DD or N/A.")
    return value

def validate_status(item_type, value):
    value = required(value, "Status").upper()
    allowed = VALID_RFI_STATUSES if item_type == "RFI" else VALID_DEF_STATUSES
    if value not in allowed:
        raise ValueError(f"Invalid {item_type} status. Allowed: {', '.join(sorted(allowed))}")
    return value
