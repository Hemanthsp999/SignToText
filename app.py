from flask import Flask, url_for, session, render_template, request, redirect
from database import connection
import bcrypt

app = Flask(__name__)
app.secret_key = 'ThisIsASecretKey'  # Ensure this is set for session management


@app.route("/")
def Home():
    if 'user' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('Login'))


@app.route("/letstalk", methods=["GET"])
def LetsTalk():
    if 'user' in session:
        return render_template("letstalk.html")
    else:
        return redirect(url_for('Login'))


@app.route("/login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Debugging print statement
        print(f"Login attempt with email: {email}")

        try:
            c, conn = connection()
            c.execute("SELECT * FROM UserDetails WHERE EMAIL=%s", [email])
            user = c.fetchone()

            if user:
                print(f"User found: {user}")  # Debugging print statement
                stored_hash = user[4]

                # Ensure stored_hash is a string
                if isinstance(stored_hash, bytes):
                    stored_hash = stored_hash.decode('utf-8')
                else:
                    print("Stored Password is not in hash")

                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    # Assuming user[1] is the username
                    session['user'] = user[1]
                    # Debugging print statement
                    print("User logged in: ", session['user'])
                    return redirect(url_for('Home'))
                else:
                    print("Password check failed")  # Debugging print statement
            else:
                print("User not found")  # Debugging print statement

            error = "Incorrect email or password"
            return render_template('auths/login.html', error=error)
        except Exception as e:
            err = f"Error occurred: {e}"
            print(err)  # Debugging print statement
            return render_template('auths/login.html', error=err)
        finally:
            if 'c' in locals() and c:
                c.close()
            if 'conn' in locals() and conn:
                conn.close()

    return render_template('auths/login.html')


@app.route('/logout')
def Logout():
    session.pop('user', None)
    print("User Loged out")
    return redirect(url_for('Login'))


@app.route("/signin", methods=["GET", "POST"])
def Signin():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phnNumber = request.form['phnNumber']
        password = request.form['password']
        radioBtn = request.form['deaf']

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
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
