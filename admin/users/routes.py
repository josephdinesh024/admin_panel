from flask import Blueprint,render_template,redirect,url_for,flash,after_this_request,request
from flask_login import login_user
from admin import db
from admin.models import User, Address
from admin.users.forms import LoginForm, ProfileForm
user = Blueprint('users',__name__)


@user.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    varify = request.args.get("varify",0,type=int)
    number = form.phone_number.data
    if varify and form.otp.data ==123456:
        user = User.query.filter_by(phone=str(number)).first()
        if user:
            login_user(user)
            print(user)
            return redirect(url_for("mains.index"))
        
        else:
            @after_this_request
            def set_cookies(response):
                res = response
                res.set_cookie("phone",str(number))
                return res           
            return redirect(url_for("users.profile"))
    return render_template("login.html",form=form)

@user.route("/profile",methods=['GET','POST'])
def profile():
    form = ProfileForm()
    phone =request.cookies.get("phone")
    print(phone)
    if form.validate_on_submit():
        add_user = User(name=form.name.data,email=form.email.data,phone=phone)
        db.session.add(add_user)
        db.session.commit()
        new_user = User.query.filter_by(name=form.name.data,email=form.email.data,phone=phone).first()
        add_address = Address(user_id=new_user.user_id,street=form.street.data,city=form.city.data,
                              state=form.state.data,postal_code=form.postal_code.data,country=form.country.data)
        db.session.add(add_address)
        db.session.commit()
        login_user(new_user)
        flash("User as Created")
        return redirect(url_for("mains.index"))
    return render_template("profile.html",form=form)
