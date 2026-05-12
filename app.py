import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from model_patient import Patient

DB = Path("/data/patients.json")
app = FastAPI()

def read():  return json.loads(DB.read_text())
def write(d): DB.write_text(json.dumps(d, indent=4, ensure_ascii=False))
def find(ssn): return next((p for p in read() if p["ssn"] == ssn), None)

@app.get("/patients")
def list_all():
    return read()

@app.post("/patients")
def create(p: Patient):
    if p.ssn[5:7] != "91":
        raise HTTPException(400, "Patient doit être né en Essonne (91)")
    if find(p.ssn):
        raise HTTPException(409, "SSN déjà enregistré")
    db = read(); db.append(p.model_dump()); write(db)
    return p

@app.get("/patients/{ssn}")
def get_one(ssn: str,
            sexe: bool = False, annee: bool = False, mois: bool = False,
            departement: bool = False, insee: bool = False, indice: bool = False):
    p = find(ssn)
    if not p: raise HTTPException(404, "Introuvable")
    info = Patient(**p).info()
    flags = {"sexe": sexe, "annee": annee, "mois": mois,
             "departement": departement, "insee": insee, "indice": indice}
    return {**p, **{k: info[k] for k, on in flags.items() if on}}

@app.delete("/patients/{ssn}")
def delete(ssn: str):
    db = read(); new = [p for p in db if p["ssn"] != ssn]
    if len(new) == len(db): raise HTTPException(404, "Introuvable")
    write(new); return {"deleted": ssn}

@app.put("/patients/{ssn}")
def update(ssn: str, p: Patient):
    db = read()
    for i, x in enumerate(db):
        if x["ssn"] == ssn:
            db[i] = p.model_dump(); write(db); return p
    raise HTTPException(404, "Introuvable")

@app.post("/patients/{ssn}")
def create_with_ssn(ssn: str, p: Patient):
    if find(p.ssn):
        raise HTTPException(409, "SSN déjà enregistré")
    db = read(); db.append(p.model_dump()); write(db)
    return p