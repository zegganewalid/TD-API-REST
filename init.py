from pathlib import Path
p = Path("/data/patients.json")
if not p.exists():
    p.write_text("[]")