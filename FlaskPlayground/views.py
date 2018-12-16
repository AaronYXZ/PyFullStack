from forms import UploadForm
from flask import request, Flask, render_template


app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def index():
    form = UploadForm()
    if request.method == "POST":
        input_file = request.files['input_file']
    else:
        return render_template("index.html", form=form)

app.run(port = 5002)
