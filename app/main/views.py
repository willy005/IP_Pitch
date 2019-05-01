from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User
from.forms import UpdateProfile
from flask_login import login_required, current_user
from .. import db, photos


# Views
@main.route('/')
def index():

    '''
    View page function that returns the index page and its data
    '''
    title = 'Pitch Perfect'

    return render_template('index.html', title=title)


@main.route('/user/')
def profile():
    user = User.query.filter_by(username = current_user.username).first()
    # all = Pitch.query.all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, all =all)


@main.route('/user/update',methods = ['GET','POST'])
@login_required
def update_profile():
    user = User.query.filter_by(username = current_user.username).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/category/business',methods = ['GET','POST'])
@login_required
def business():
    user = User.query.filter_by(username = current_user.username).first()

    if user is None:
        abort(404)

    return render_template("category/business.html", user = user)


@main.route('/category/entertainment',methods = ['GET','POST'])
@login_required
def entertainment():
    user = User.query.filter_by(username = current_user.username).first()

    if user is None:
        abort(404)

    return render_template("category/entertainment.html", user = user)


@main.route('/category/school',methods = ['GET','POST'])
@login_required
def school():
    user = User.query.filter_by(username = current_user.username).first()

    if user is None:
        abort(404)

    return render_template("category/school.html", user = user)


@main.route('/user/update/pic',methods= ['POST'])
@login_required
def update_pic():
    user = User.query.filter_by(username = current_user.username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=current_user.username))


