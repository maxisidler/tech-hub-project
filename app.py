from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

class Catalogo:
    def __init__(self, host, user, password, database, port):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.conector = self.conn.cursor(dictionary=True)
        self.conector.execute('''CREATE TABLE IF NOT EXISTS productos (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255),
            proveedor INT)''')
        self.conn.commit()

    def agregar_producto(self, descripcion, cantidad, precio, imagen_url, proveedor):
        sql = "INSERT INTO productos (descripcion, cantidad, precio, imagen_url, proveedor) VALUES (%s, %s, %s, %s, %s)"
        self.conector.execute(sql, (descripcion, cantidad, precio, imagen_url, proveedor))
        self.conn.commit()
        return True

    def consultar_producto(self, codigo):
        self.conector.execute("SELECT * FROM productos WHERE codigo = %s", (codigo,))
        return self.conector.fetchone()

    def modificar_producto(self, codigo, descripcion, cantidad, precio, imagen_url, proveedor):
        sql = "UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s, imagen_url = %s, proveedor = %s WHERE codigo = %s"
        self.conector.execute(sql, (descripcion, cantidad, precio, imagen_url, proveedor, codigo))
        self.conn.commit()
        return self.conector.rowcount > 0

    def listar_productos(self):
        self.conector.execute("SELECT * FROM productos")
        return self.conector.fetchall()

    def eliminar_producto(self, codigo):
        self.conector.execute("DELETE FROM productos WHERE codigo = %s", (codigo,))
        self.conn.commit()
        return self.conector.rowcount > 0

catalogo = Catalogo(host='localhost', user='root', password='', database='miapp', port=3309)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stock')
def crud():
    return render_template('admin/stock.html')

@app.route('/about')
def about():
    return render_template('shop/about.html')

@app.route('/contact')
def contact():
    return render_template('shop/contact.html')

@app.route('/shop')
def shop():
    return render_template('shop/shop.html')

@app.route('/productos', methods=['GET'])
def listar_productos():
    productos = catalogo.listar_productos()
    return jsonify(productos)

@app.route('/producto/<int:codigo>', methods=['GET'])
def consultar_producto(codigo):
    producto = catalogo.consultar_producto(codigo)
    if producto:
        return jsonify(producto)
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/producto', methods=['POST'])
def agregar_producto():
    data = request.json
    catalogo.agregar_producto(data['descripcion'], data['cantidad'], data['precio'], data['imagen_url'], data['proveedor'])
    return jsonify({"message": "Producto agregado exitosamente"}), 201

@app.route('/producto/<int:codigo>', methods=['PUT'])
def modificar_producto(codigo):
    data = request.json
    if catalogo.modificar_producto(codigo, data['descripcion'], data['cantidad'], data['precio'], data['imagen_url'], data['proveedor']):
        return jsonify({"message": "Producto modificado exitosamente"})
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/producto/<int:codigo>', methods=['DELETE'])
def eliminar_producto(codigo):
    if catalogo.eliminar_producto(codigo):
        return jsonify({"message": "Producto eliminado exitosamente"})
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
