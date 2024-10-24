from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id
    
    def __str__(self) -> str:
        return self.id.__str__() + ' | ' + self.content + ' | ' + self.completed.__str__() + ' | ' + self.date_created.__str__()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_req = request.form['content']
        new_task = Todo(content=task_req)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error while trying to add your Task'
    else:
        # return Todo.query.order_by(Todo.date_created).all().__str__()
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
        #return render_template('index.html')

@app.route("/new")
def newPage():
    return "GYM!"

@app.route("/delete/<int:id>")
def delete(id):
    task = db.session.query(Todo).get(id)
    
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Error Deleting Task with id: " + str(id)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get(id)

    if request.method == 'GET':
        return render_template('update.html', task=task)
    else:
        taskToUpdate = request.form['content']
        task.content = taskToUpdate
        db.session.commit()
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
