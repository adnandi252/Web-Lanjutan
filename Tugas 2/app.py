from flask import Flask, request, jsonify
import mysql.connector
from jwt_auth import setup_jwt, generate_access_token
from flask_jwt_extended import jwt_required


app = Flask(__name__)
setup_jwt(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_repositori"
)

@app.route('/', methods=['GET'])
def index():
    return jsonify(message='Selamat Datang di sini')


#Login
@app.route('/login', methods=['POST'])
def login():
    nama_lengkap = request.json.get('nama_lengkap')
    nip = request.json.get('nip')
    
    cursor = db.cursor()
    sql = "SELECT * FROM data_dosen WHERE nama_lengkap = %s AND nip = %s"
    cursor.execute(sql, (nama_lengkap, nip))
    dosen = cursor.fetchone()

    if dosen:
        access_token = generate_access_token(identity=dosen[1])
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Nama lengkap atau NIP tidak teridentifikasi"), 401


# Create
@app.route('/create_prodi', methods=['POST'])
@jwt_required()
def create_prodi():
    data_list = request.json
    cursor = db.cursor()
    sql = "INSERT INTO data_prodi (kode_prodi, nama_prodi) VALUES (%s, %s)"

    for data in data_list:
        val = (data['kode_prodi'], data['nama_prodi'])
        cursor.execute(sql, val)

    db.commit()
    return jsonify({'message': 'Data prodi berhasil ditambahkan'})


@app.route('/create_dosen', methods=['POST'])
@jwt_required()
def create_dosen():
    data_list = request.json
    cursor = db.cursor()
    sql = "INSERT INTO data_dosen (nip, nama_lengkap, prodi_id) VALUES (%s, %s, %s)"
    for data in data_list:
        val = (data['nip'], data['nama_lengkap'], data['prodi_id'])
        cursor.execute(sql, val)
    db.commit()
    return jsonify({'message': 'Data dosen berhasil ditambahkan'})

@app.route('/create_dokumen', methods=['POST'])
@jwt_required()
def create_dokumen():
    data_list = request.json
    cursor = db.cursor()
    for data in data_list:
        sql = "INSERT INTO data_dokumen (nip, type_dokumen, nama_dokumen, nama_file) VALUES (%s, %s, %s, %s)"
        val = (data['nip'], data['type_dokumen'], data['nama_dokumen'], data['nama_file'])
    cursor.execute(sql, val)
    db.commit()
    return jsonify({'message': 'Data dokumen berhasil ditambahkan'})

# Read
@app.route('/read_prodi', methods=['GET'])
@jwt_required()
def read_prodi():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_prodi")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/read_dosen', methods=['GET'])
@jwt_required()
def read_dosen():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_dosen")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/read_dokumen', methods=['GET'])
@jwt_required()
def read_dokumen():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_dokumen")
    result = cursor.fetchall()
    return jsonify(result)

# Update
@app.route('/update_prodi/<string:id>', methods=['PUT'])
@jwt_required()
def update_prodi(id):
    data_list = request.json
    data = data_list[0]
    cursor = db.cursor()
    sql = "UPDATE data_prodi SET nama_prodi = %s, kode_prodi = %s WHERE id = %s"
    val = (data.get('nama_prodi'), data.get('kode_prodi'), id)
    cursor.execute(sql, val)
    db.commit()
    return jsonify({'message': 'Data prodi berhasil diupdate'})

@app.route('/update_dosen/<string:nip>', methods=['PUT'])
@jwt_required()
def update_dosen(nip):
    data_list = request.json
    data = data_list[0]
    cursor = db.cursor()
    sql = "UPDATE data_dosen SET nama_lengkap = %s, prodi_id = %s WHERE nip = %s"
    val = (data['nama_lengkap'], data['prodi_id'], nip)
    cursor.execute(sql, val)
    db.commit()
    return jsonify({'message': 'Data dosen berhasil diupdate'})

@app.route('/update_dokumen/<string:id>', methods=['PUT'])
@jwt_required()
def update_dokumen(id):
    data_list = request.json
    cursor = db.cursor()
    data = data_list[0]
    sql = "UPDATE data_dokumen SET type_dokumen = %s, nama_dokumen = %s, nama_file = %s, nip = %s WHERE id = %s"
    val = (data['type_dokumen'], data['nama_dokumen'], data['nama_file'], data['nip'], id)
    cursor.execute(sql, val)
    db.commit()
    return jsonify({'message': 'Data dokumen berhasil diupdate'})

# Delete
@app.route('/delete_prodi/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_prodi(id):
    cursor = db.cursor()
    sql = "DELETE FROM data_prodi WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    db.commit()
    return jsonify({'message': 'Data prodi berhasil dihapus'})

@app.route('/delete_dosen/<string:nip>', methods=['DELETE'])
@jwt_required()
def delete_dosen(nip):
    cursor = db.cursor()
    sql = "DELETE FROM data_dosen WHERE nip = %s"
    val = (nip,)
    cursor.execute(sql, val)
    db.commit()
    return jsonify({'message': 'Data dosen berhasil dihapus'})

@app.route('/delete_dokumen/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_dokumen(id):
    cursor = db.cursor()
    sql = "DELETE FROM data_dokumen WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    db.commit()
    return jsonify({'message': 'Data dokumen berhasil di hapus'})

if __name__ == '__main__':
    app.run(debug=True)
