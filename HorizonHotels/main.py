from flask import Flask, render_template, request, redirect, url_for, session, flash

# Create the Flask app
app = Flask(__name__) 
app.secret_key = 'your_secret_key'  

# For home page, check to see if session contains username, if not User needs to login
@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

# Gets input from form in login page, 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Checks if username and password are not empty
        if username and password: 
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')


# Gets input from form in signup page, checks if password and confirm password match
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('signup.html')
            
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('signup.html')

# For booking page, same come as to chceck if logged in
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('booking.html')

#clears session data to log user out
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
