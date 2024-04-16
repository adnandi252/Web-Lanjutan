from pydantic import BaseModel

class Dosen(BaseModel):
    __tablename__ = 'data_dosen'
    nip: str
    nama_lengkap: str
    prodi_id: int


class Prodi(BaseModel):
    __tablename__ = 'data_prodi'
    kode_prodi: str
    nama_prodi: str

class Dokumen(BaseModel):
    __tablename__ = 'data_dokumen'
    nip: str
    type_dokumen: str
    nama_dokumen: str
    nama_file: str

class User(BaseModel):
    nip: str
    nama_lengkap: str