from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



#my app
app = Flask(__name__)
Scss(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#data class
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self) -> str:
        return f"<Task {self.id}>"


#routes
#homepage
@app.route("/", methods=["POST", "GET"])
def index():
    
    #add task
    if request.method == "POST":
        current_task = request.form["content"]
        new_task = MyTask(content=current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            print(f"Error:(e)")
            return ("Error:(e)")
    #see all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created_at).all()
        return render_template("index.html", tasks=tasks)



if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

