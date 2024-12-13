import ast
from PIL import Image
from flask import Flask, request, render_template, redirect, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_folder="public")

session = {"authenticated": False, "username": ""}

ALLOWED_USERS = {"admin": "admin"}

wallpapers = {}

DATABASE_FILE = "public/database.txt"

def create_thumbnails():
    for theme, files in wallpapers.items():
        for file in files:
            original_image_path = os.path.join('public', 'wallpapers', theme, file)
            extension = file.split('.')[-1]
            file_name = file.split('.')[0]
            thumbnail_dir = os.path.join('public', 'wallpapers', theme)
            thumbnail_path = os.path.join(thumbnail_dir, f'{file_name}.thumb.png')

            if os.path.exists(thumbnail_path):
                continue

            original_image = Image.open(original_image_path)
            original_image.thumbnail((200, 200))
            original_image.save(thumbnail_path, "PNG")

            try:
                if not os.path.exists(thumbnail_path):
                    os.makedirs(thumbnail_dir, exist_ok=True)

            except Exception as e:
                return "Error creating thumbnails", 500

@app.route("/")
def index():
    return render_template("index.html", wallpapers=wallpapers, session=session)

@app.route('/about')
def about():
    return render_template('about.html', session=session)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get("authenticated", False):
        return redirect("/login")

    if request.method == 'POST':
        file = request.files.get('image')
        theme = request.form.get("category", "")
        if theme == "custom":
            theme = request.form.get("custom_theme", "")
            os.makedirs(os.path.join("public/wallpapers", theme), exist_ok=True)
        new_name = request.form.get("name", "")

        if not os.path.exists(os.path.join("public/wallpapers", theme)):
            os.makedirs(os.path.join("public/wallpapers", theme))

        if new_name:
            name = secure_filename(new_name + "." + file.filename.split('.')[-1])
        else:
            name = secure_filename(file.filename)

        if file and allowed_file(file.filename) and theme:
            save_path = os.path.join("public/wallpapers", theme, name)

            if os.path.exists(save_path):
                return redirect("/upload")

            file.save(save_path)

            current_files = wallpapers.get(theme, [])
            current_files.append(name)
            wallpapers[theme] = current_files

            write_database(DATABASE_FILE)
            read_database(DATABASE_FILE)

            return redirect('/upload')

    predefined_themes = list(wallpapers.keys())

    return render_template('upload.html', predefined_themes=predefined_themes, session=session)

@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if ALLOWED_USERS.get(username) == password:
            session["authenticated"] = True
            session["username"] = username
            return redirect("/")
        else:
            error_msg = "Wrong username or password. Please try again."
            pass
    return render_template("login.html", session=session, error_msg=error_msg)

@app.route("/logout")
def logout():
    if not session["authenticated"]:
        return redirect("/")

    session["authenticated"] = False
    session["username"] = ""
    return redirect("/")

@app.route('/delete_image', methods=['POST'])
def delete_image():
    theme = request.form['theme']
    image_path = request.form['image_path']
    
    full_image_path = os.path.join('public', 'wallpapers', theme, image_path)
    thumbnail_path = os.path.join('public', 'wallpapers', theme, f'{image_path.split(".")[0]}.thumb.png')
    
    try:
        if os.path.exists(full_image_path):
            os.remove(full_image_path)
            os.remove(thumbnail_path)
            wallpapers[theme].remove(image_path)

            if not wallpapers[theme]:
                wallpapers.pop(theme)
                os.rmdir(os.path.join('public', 'wallpapers', theme))

            write_database(DATABASE_FILE)
            read_database(DATABASE_FILE)
    except Exception as e:
        return "Error creating thumbnails", 500


    return redirect('/')

@app.route('/delete_all_images', methods=['POST'])
def delete_all_images():
    theme = request.form['theme']
    
    theme_dir = os.path.join('public', 'wallpapers', theme)
    
    try:
        for image_path in wallpapers.get(theme, []):
            full_image_path = os.path.join(theme_dir, image_path)
            if os.path.exists(full_image_path):
                os.remove(full_image_path)
        
        wallpapers[theme] = []

        wallpapers.pop(theme)
        os.rmdir(theme_dir)

        write_database(DATABASE_FILE)
        read_database(DATABASE_FILE)
        
    except Exception as e:
        return "Error creating thumbnails", 500


    return redirect('/')

def read_database(filename):
    global wallpapers

    with open(filename, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                theme, files = stripped_line.split(": ", 1)
                theme = theme.strip('"')
                files = ast.literal_eval(files.rstrip(','))
                files.sort()
                wallpapers[theme] = files

    return dict(sorted(wallpapers.items()))

def write_database(filename):
    global wallpapers
    
    try:
        with open("public/tmp", "a") as file:
            file.seek(0)
            for theme, files in wallpapers.items():
                file.write(f'"{theme}": {files},\n')
    except Exception as e:
        return "Error creating thumbnails", 500


    file.close()

    file = open("public/tmp", "r")
    content = file.read()
    file.close()
    os.remove("public/tmp")

    file = open(filename, "w")
    file.write(content)
    file.close()

@app.errorhandler(404)
def error404(code):
    return "HTTP Error 404 - Page Not Found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

