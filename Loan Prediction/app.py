from flask import Flask, request, render_template,flash, redirect, url_for
import pickle
import numpy as np
import sklearn 

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():                                                                                                                                                                                                
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        loan = request.form['loan']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

# Transformation
    # gender
        if (gender =="Male"):
            male=1
        else:
            male=0

    # married
        if (married=="Yes"):
            married_yes=1
        else:
            married_yes=0
    
    # dependents
        if (dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif (dependents=='2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif (dependents=='3+'):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0

    # education
        if (education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

    # employed
        if (employed=="Yes"):
            employed_yes=1
        else:
            employed_yes=0

    # property area
        if (area=="Semiurban"):
            semiurban=1
            urban=0
        elif(area=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0
    # loan status
        if (loan=="Y"):
            loan_y=1
        else:
            loan_y=0

        ApplicantIncomelog = np.log(ApplicantIncome) 
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)  

        prediction = model.predict([[credit, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Termlog, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes,semiurban,urban]])  

        if (prediction=="N"):
            prediction="No"
        else:
            prediction="Yes"

        return render_template("prediction.html", prediction_text="Loan status is {}".format(prediction))

    else :
        return render_template("prediction.html")

@app.route('/about')
def about():
    return render_template("aboutus.html")

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/check_eligibility', methods=['POST','GET'])
def check_eligibility():
    if request.method == 'POST':
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        employed = request.form['employed']
        credit = float(request.form['credit'])

    # Example simple eligibility criteria
        if ApplicantIncome >= 25000 and CoapplicantIncome >= 25000 and employed >= "Yes" and credit >= 600:
            result = "Congratulations! You are eligible for the loan."
        else:
            result = "Sorry, you do not meet the eligibility criteria for the loan."

        return render_template('result.html', result=result)
    else :
        return render_template("check_eligibility.html")

@app.route('/eligibility')
def eligibility():
    return render_template('eligibility.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('number')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Normally, you would process/store the form data here
        
        flash('Thank you for contacting us! We will get back to you shortly.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

app.secret_key = 'your_secret_key'  # Required for flash messages

# Dummy in-memory user store
users = {}


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('User already exists! Please login.', 'danger')
            return redirect(url_for('signin'))

        users[username] = password
        flash('Registration Successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users.get(username) == password:
            flash('Login Successful!', 'success')
            return "Welcome to Loan Approval Dashboard!"  # Placeholder
        else:
            flash('Invalid Credentials. Try Again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form.get("email")
        if email:  
            # Here you would normally send a reset link via email
            flash("A password reset link has been sent to your email.", "success")
            return redirect(url_for("forgot"))
        else:
            flash("Please enter a valid email address.", "danger")
    return render_template("forgot.html")

if __name__ == "__main__":
    app.run(debug=True)