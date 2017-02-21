from flask import Flask, render_template, request
from werkzeug import secure_filename
import os

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = '/home/maielld1/mysite/tmp/'
ALLOWED_EXTENSIONS = set(['csv'])
order = ['PG', 'SG', 'SF', 'PF', 'C', 'G', 'F', 'U']
points=0
salary=0

def allowed_file(filename):
    """Does filename have the right extension?"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET", "POST"])
def index():
    filename = None  # default
    total_sal = 0
    total_pts = 0
    name=[]
    salary=[]
    points=[]
    if request.method == "POST":
        if request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                # Make a valid version of filename for any file ystem
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        import optimizerNBA
        team = optimizerNBA.optimize()

        for p in order:
            name.append(team[p].name)
            salary.append(str(team[p].salary))
            points.append(str(team[p].points))
            total_sal+=team[p].salary
            total_pts+=team[p].points

    return render_template("index.html", order=order, name=name, salary=salary, points=points, total_sal=total_sal, total_pts=total_pts)
