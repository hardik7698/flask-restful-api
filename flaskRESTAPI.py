from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init
app= Flask(__name__)

basedir = os.getcwd()

#Database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' +os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#init db
db=SQLAlchemy(app)
#init ma
ma=Marshmallow(app)

#Product Class/Model
class Product(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    name=db.Column(db.String(100),unique=True)
    desc=db.Column(db.String(200))
    price=db.Column(db.Float)
    qty=db.Column(db.Integer)

    def __init__(self,name,desc,price,qty):
        self.name=name
        self.desc=desc
        self.price=price
        self.qty=qty

#prod schema

class ProductSchema(ma.Schema):
    class Meta:
        fields =('id','name','desc','price','qty')
#init Schema
prod_schema=ProductSchema()
products_schema=ProductSchema(many=True)

#create a prod

@app.route('/product',methods=['POST'])
def addProduct():
    name =request.json['name']
    desc =request.json['desc']
    price =request.json['price']
    qty =request.json['qty']

    new_product=Product(name,desc,price,qty)

    db.session.add(new_product)
    db.session.commit()

    return prod_schema.jsonify(new_product)

#get products

@app.route('/products',methods=['GET'])
def getProducts():
    all_products=Product.query.all()
    results=products_schema.dump(all_products)
    print(results)
    return jsonify(results)

#get one product

@app.route('/products/<id>',methods=['GET'])
def getProduct(id):
    product=Product.query.get(id)
    return prod_schema.jsonify(product)

#update a prod

@app.route('/product/<id>',methods=['PUT'])
def updateProduct(id):
    product=Product.query.get(id)
    name =request.json['name']
    desc =request.json['desc']
    price =request.json['price']
    qty =request.json['qty']
    product.name=name
    product.desc=desc
    product.price=price
    product.qty=qty
    db.session.commit()

    return prod_schema.jsonify(product)

#delete  product

@app.route('/products/<id>',methods=['DELETE'])
def deleteProduct(id):
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return prod_schema.jsonify(product)
#run Server
if __name__=='__main__':
    app.run(debug=True)
