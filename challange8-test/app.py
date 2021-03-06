from flask import Flask,render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient

client = MongoClient('127.0.0.1',27017)
mdb = client.tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/li'
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category',backref=db.backref('file',lazy = 'dynamic'))

    def __init__(self,title,content,category_time = None):
        self.title = title
        self.content = content
        if category_time == None:
            category_time = datetime.utcnow()
        self.category_time = category_time
    def __repr__(self):
        return '<File %r>'%self.title
    def add_tag(self,tag_name):
        tag = {'id':self.id,'tag':tag_name}
        mdb.tag.insert_one(tag)
    def remove_tag(self,tag_name):
        mdb.tag.remove({'tag':tag_name})
    @property
    def tag(self):
        return mdb.tag.find()

class Category(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80))
    
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' %self.name
class Test(db.Model):
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80))
    
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Test %r>' %self.name
java = Category('Java')
python = Category('Python')
file1 = File('Hello Java','File Content - Java is cool!',datetime.utcnow())
file2 = File('Hello python','File Content - Python is cool!',datetime.utcnow())
db.session.add(java)
db.session.add(python)
db.session.add(file1)
db.session.add(file2)
db.session.commit()
file1.add_tag('tech')
file1.add_tag('java')
file1.add_tag('linux')
file2.add_tag('tech')
file2.add_tag('python')

@app.route('/')
def index():
    return render_template('index.html',tag = File.tags(),files = File.query.all())

@app.route('/files/<file_id>')
def file(file_id):
    file_item = File.query.get_or_404(file_id)
    return render_template('files.html',file_item=file_item)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run()
