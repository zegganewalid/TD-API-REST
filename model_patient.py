from pydantic import BaseModel, field_validator

class Patient(BaseModel):
    nom: str
    prenom: str
    ssn: str

    @field_validator("ssn")
    @classmethod
    def check_ssn(cls, v: str) -> str:
        if not v.isdigit() or len(v) != 15:
            raise ValueError("SSN doit faire 15 chiffres")
        if v[0] not in ("1", "2"):
            raise ValueError("1er chiffre = 1 (H) ou 2 (F)")
        if not 1 <= int(v[3:5]) <= 12:
            raise ValueError("Mois invalide")
        if 97 - int(v[:13]) % 97 != int(v[13:15]):
            raise ValueError("Clef de contrôle invalide")
        return v

    def info(self) -> dict:
        return {
            "sexe": "homme" if self.ssn[0] == "1" else "femme",
            "annee": int(self.ssn[1:3]),
            "mois": int(self.ssn[3:5]),
            "departement": self.ssn[5:7],
            "insee": self.ssn[7:10],
            "indice": self.ssn[10:13],
        }