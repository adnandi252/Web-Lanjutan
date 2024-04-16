from fastapi import Depends, FastAPI, HTTPException, Request
import mysql.connector
from jwt_auth import create_access_token, decode_token
from models import *


app = FastAPI()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_repositori"
)

def authenticate_login(token: str = Depends(decode_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token tidak valid")
        return token
    
@app.post("/login/")
async def login(data: User):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_dosen WHERE nama_lengkap = %s AND nip = %s", (data.nama_lengkap, data.nip))
    user = cursor.fetchone()
    
    if user:
        access_token = create_access_token({"nama_lengkap": user[1], "nip": user[0]})
        return {"access_token": access_token, "message": "LOGIN BERHASIL!!!"}
    else:
        raise HTTPException(status_code=401, detail="Nama lengkap atau NIP tidak teridentifikasi")
    
# Create data_prodi
@app.post("/prodi/")
async def create_prodi(data_prodi: Prodi, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    query = "INSERT INTO data_prodi (kode_prodi, nama_prodi) VALUES (%s, %s)"
    cursor.execute(query, (data_prodi.kode_prodi, data_prodi.nama_prodi))
    db.commit()
    return {"message": "Data prodi berhasil ditambahkan"}

# Read data_prodi
@app.get("/prodi/{id}")
async def read_prodi(id: int, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_prodi WHERE id = %s", (id,))
    prodi = cursor.fetchone()
    
    if prodi:
        return {"kode_prodi": prodi[1], "nama_prodi": prodi[2]}
    else:
        raise HTTPException(status_code=404, detail="Data prodi tidak ditemukan")
    
# Update data_prodi
@app.put("/prodi/{id}")
async def update_prodi(id: int, data_prodi: Prodi, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    query = "UPDATE data_prodi SET kode_prodi = %s, nama_prodi = %s WHERE id = %s"
    cursor.execute(query, (data_prodi.kode_prodi, data_prodi.nama_prodi, id))
    db.commit()
    return {"message": "Data prodi berhasil diperbarui"}

# Delete data_prodi
@app.delete("/prodi/{id}")
async def delete_prodi(id: int, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM data_prodi WHERE id = %s", (id,))
    db.commit()
    return {"message": "Data prodi berhasil dihapus"}

# Create data_dosen
@app.post("/dosen/")
async def create_dosen(data_dosen: Dosen, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    query = "INSERT INTO data_dosen (nip, nama_lengkap, prodi_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (data_dosen.nip, data_dosen.nama_lengkap, data_dosen.prodi_id))
    db.commit()
    return {"message": "Data dosen berhasil ditambahkan"}

# Read data_dosen
@app.get("/dosen/{nip}")
async def read_dosen(nip: str, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_dosen WHERE nip = %s", (nip,))
    dosen = cursor.fetchone()
    
    if dosen:
        return {"nip": dosen[0], "nama_lengkap": dosen[1], "prodi_id": dosen[2]}
    else:
        raise HTTPException(status_code=404, detail="Data dosen tidak ditemukan")
    
# Update data_dosen
@app.put("/dosen/{nip}")
async def update_dosen(nip: str, data_dosen: Dosen, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    query = "UPDATE data_dosen SET nip = %s, nama_lengkap = %s, prodi_id = %s WHERE nip = %s"
    cursor.execute(query, (data_dosen.nip, data_dosen.nama_lengkap, data_dosen.prodi_id, nip))
    db.commit()
    return {"message": "Data dosen berhasil diperbarui"}

# Delete data_dosen
@app.delete("/dosen/{nip}")
async def delete_dosen(nip: str, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM data_dosen WHERE nip = %s", (nip,))
    db.commit()
    return {"message": "Data dosen berhasil dihapus"}

# Create data_dokumen
@app.post("/dokumen/")
async def create_dokumen(data_dokumen: Dokumen, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    query = "INSERT INTO data_dokumen (nip, type_dokumen, nama_dokumen, nama_file) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (data_dokumen.nip, data_dokumen.type_dokumen, data_dokumen.nama_dokumen, data_dokumen.nama_file))
    db.commit()
    return {"message": "Data dokumen berhasil ditambahkan"}

# Read data_dokumen
@app.get("/dokumen/{id}")
async def read_dokumen(id: int, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_dokumen WHERE id = %s", (id,))
    dokumen = cursor.fetchone()
    
    if dokumen:
        return {"nip": dokumen[1], "type_dokumen": dokumen[2], "nama_dokumen": dokumen[3], "nama_file": dokumen[4]}
    else:
        raise HTTPException(status_code=404, detail="Data dokumen tidak ditemukan")
    
# Update data_dokumen
@app.put("/dokumen/{id}")
async def update_dokumen(id: int, data_dokumen: Dokumen, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    query = "UPDATE data_dokumen SET nip = %s, type_dokumen = %s, nama_dokumen = %s, nama_file = %s WHERE id = %s"
    cursor.execute(query, (data_dokumen.nip, data_dokumen.type_dokumen, data_dokumen.nama_dokumen, data_dokumen.nama_file, id))
    db.commit()
    return {"message": "Data dokumen berhasil diperbarui"}

# Delete data_dokumen
@app.delete("/dokumen/{id}")
async def delete_dokumen(id: int, token: dict = Depends(authenticate_login)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM data_dokumen WHERE id = %s", (id,))
    db.commit()
    return {"message": "Data dokumen berhasil dihapus"}