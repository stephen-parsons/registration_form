# Stephen Parsons
# Assignment Registration Form
# 12/3/17

from flask import Flask, render_template, request, redirect, flash, session
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "myKey"
@app.route('/')
def index():
	return render_template('index.html')
@app.route('/process', methods=["POST"])
def get_info():
	print request.form
	for error in request.form:
		if error == "first_name" or error == "last_name":
			for char in request.form[error]:
				if str(char).isdigit():
				 	flash("No numbers in the name fields!")
					return redirect('/') 
		if error == "password":
			if len(request.form[error]) < 8:
				flash("Password must be at least 8 characters long!")
				return redirect('/')		
		if error == "email":
			if not EMAIL_REGEX.match(request.form['email']):
				flash("Please enter a valid email address!")
				return redirect('/')
		if error == "password":
			digit = False
			upper = False
			for char in request.form[error]:
				if str(char).isdigit():
					digit = True
				if not str(char).isdigit() and not str(char).islower():	
					upper = True
			if digit == False or upper == False: 	
			 	flash("Password MUST contain at least one number and one uppercase letter!")
				return redirect('/') 
			if request.form[error] != request.form["confirm"]:
				flash("Passwords must match!")
				return redirect('/')
		if len(request.form[error]) < 1:
			flash("Please fill out ALL fields!") # just pass a string to the flash function
			return redirect('/')
	if '_flashes' not in session:
		flash("Success! Got info!")
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		email = request.form['email']
		password = request.form['password']
		confirm = request.form['confirm']
		# birthday = request.form['birthday']
		return render_template('process.html', first_name=first_name, last_name=last_name, email=email)
@app.route('/back', methods=["POST"])
def back():
	session.pop('_flashes', None)
	return redirect('/')		
app.run(debug=True)		