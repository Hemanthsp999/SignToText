from flask import Flask, url_for, session, render_template, request, redirect, jsonify
from database import connection
from ultralytics import YOLO
import bcrypt
import base64
import io
from PIL import Image

app = Flask(__name__)
# Ensure this is set for session management
app.secret_key = 'ThisIsASecretKeyYou'

model = YOLO("runs/detect/train3/weights/best.pt")

prediction_buffer = []


@app.route("/")
def Home():
    if 'user' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('Login'))


@app.route("/processFrame", methods=["POST"])
def processFrame():
    if 'user' in session:
        data = request.get_json()

        if not data:
            print("No json data received")
            return jsonify({"status": "error", "message": "No Json data provided"}), 400

        if 'image' not in data:
            print("No image data provided")
            return jsonify({"status": "error", "message": "No image data provided"}), 400

        try:
            image_data = data['image']
            if image_data:
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
                print("Image Decoded Successfully")

                print("Running model prediction...")

                results = model(image)

                predictions = []

                if results:
                    print("Results found, processing predictions...")
                    for result in results:
                        if hasattr(result, 'boxes'):
                            for box in result.boxes:
                                label_index = int(box.cls[0])
                                label = model.names[label_index]
                                confidence = float(box.conf[0])
                                predictions.append(
                                    {"label": label, "confidence": confidence})

                if not predictions:
                    print("No predictions made.")
                    return jsonify({"status": "error", "message": "No sign language gesture detected"}), 400

                # append new predictions to buffer
                for pred in predictions:
                    prediction_buffer.append(pred['label'])

                predict_text = ''.join(prediction_buffer)
                print("Prediction\t ", predict_text)
                return jsonify({"status": "success", "predictions": predict_text})

        except Exception as e:
            print(f"Error processing frames: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "user not authenticated"}), 401


@ app.route("/letstalk", methods=["GET", "POST"])
def LetsTalk():
    if 'user' in session:
        return render_template("letstalk.html")
    else:
        return redirect(url_for('Login'))


@ app.route("/login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            c, conn = connection()
            c.execute("SELECT * FROM UserDetails WHERE EMAIL=%s", [email])
            user = c.fetchone()

            if user:
                stored_hash = user[4]

                if isinstance(stored_hash, bytes):
                    stored_hash = stored_hash.decode('utf-8')

                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    session['user'] = user[1]
                    return redirect(url_for('Home'))
            error = "Incorrect email or password"
            return render_template('auths/login.html', error=error)
        except Exception as e:
            err = f"Error occurred: {e}"
            return render_template('auths/login.html', error=err)
        finally:
            if 'c' in locals() and c:
                c.close()
            if 'conn' in locals() and conn:
                conn.close()

    return render_template('auths/login.html')


@ app.route('/logout')
def Logout():
    session.pop('user', None)
    return redirect(url_for('Login'))


@ app.route("/signin", methods=["GET", "POST"])
def Signin():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phnNumber = request.form['phnNumber']
        password = request.form['password']
        rePassword = request.form['re-password']
        radioBtn = request.form['deaf']

        if password == rePassword:
            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            return "Enter correct password "

        c, con = connection()

        try:
            if len(phnNumber) == 10:
                c.execute("INSERT INTO UserDetails(NAME, EMAIL, PHONE_NUMBER, PASSWORD, DEAF) VALUES (%s, %s, %s, %s, %s)",
                          (name, email, phnNumber, hashed_password, radioBtn))
                con.commit()
                return redirect(url_for('Login'))
            else:
                return "Error"

        except Exception as e:
            con.rollback()
            return f"An error occurred: {e}"
        finally:
            con.close()
    else:
        return render_template("auths/signin.html")


if __name__ == "__main__":
    app.run(debug=True)
