from tracker import ProjectTracker
from reports import ReportGenerator

def ask(prompt, default=""):
    value = input(f"{prompt}" + (f" [{default}]" if default else "") + ": ").strip()
    return value or default

def main():
    tracker = ProjectTracker()
    reports = ReportGenerator(tracker)

    while True:
        print("\n=== RFI & CONSTRUCTION DEFICIENCY TRACKER ===")
        print("1. Create RFI")
        print("2. Add deficiency")
        print("3. Update item status")
        print("4. List RFIs")
        print("5. List deficiencies")
        print("6. View open / overdue items")
        print("7. Export reports")
        print("8. Exit")
        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                data = {
                    "project": ask("Project name"),
                    "subject": ask("RFI subject"),
                    "question": ask("Technical question / clarification requested"),
                    "spec_section": ask("Specification / drawing reference", "N/A"),
                    "location": ask("Building / area / grid"),
                    "submitted_by": ask("Submitted by"),
                    "assigned_to": ask("Assigned to (designer / engineer / GC)"),
                    "due_date": ask("Response due date (YYYY-MM-DD)", "N/A"),
                    "priority": ask("Priority (Low/Medium/High)", "Medium"),
                }
                item_id = tracker.create_rfi(data)
                print(f"RFI created: {item_id}")
            elif choice == "2":
                data = {
                    "project": ask("Project name"),
                    "title": ask("Deficiency title"),
                    "description": ask("Description of observed condition"),
                    "location": ask("Building / area / grid"),
                    "trade": ask("Responsible trade"),
                    "drawing_spec": ask("Drawing / specification reference", "N/A"),
                    "reported_by": ask("Reported by"),
                    "assigned_to": ask("Assigned contractor / person"),
                    "due_date": ask("Correction due date (YYYY-MM-DD)", "N/A"),
                    "priority": ask("Priority (Low/Medium/High)", "Medium"),
                }
                item_id = tracker.create_deficiency(data)
                print(f"Deficiency created: {item_id}")
            elif choice == "3":
                item_type = ask("Item type (RFI/DEF)").upper()
                item_id = ask("Item ID")
                status = ask("New status")
                note = ask("Update note / response / corrective action")
                tracker.update_status(item_type, item_id, status, note)
                print("Status updated.")
            elif choice == "4":
                reports.list_items("RFI")
            elif choice == "5":
                reports.list_items("DEF")
            elif choice == "6":
                reports.list_open_overdue()
            elif choice == "7":
                paths = reports.export_all()
                print("Reports exported:")
                for path in paths:
                    print(f" - {path}")
            elif choice == "8":
                print("Goodbye.")
                break
            else:
                print("Please select a valid option.")
        except (ValueError, KeyError) as exc:
            print(f"Error: {exc}")

if __name__ == "__main__":
    main()
