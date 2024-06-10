from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, request, session, flash
from flask_app.models.users_model import Users
from flask_app.models.animes_model import Animes
from flask_app.models.reviews_model import Reviews

## applies to anime post html page ##
@app.route('/user/post_an_anime')
def route_to_post_show_to_veiw():
    if 'new_user_id' not in session:
        return redirect ('/')
    user_id = session['new_user_id']
    all_users = Users.get_all_users()
    print('RRRRR', user_id)
    return render_template('post_an_anime.html', users = all_users, user_id = user_id)


## applies to form INSIDE OF anime post html page ##
@app.route('/post_to_view', methods = ['POST'])
def post_anime_to_veiw():
    if not Animes.validate_anime_towatch(request.form):
        return redirect('/user/post_an_anime') 
    Animes.add_an_anime(request.form)

    return redirect('/user/profile') 

@app.route('/anime/display/<int:id>')
def display_this_anime(id):
    if 'new_user_id' not in session:
        return redirect ('/')
    this_anime = Animes.get_anime_by_id(id)
    an_anime = Animes.get_anime_w_user(id)
    return render_template('view_anime.html', anime = this_anime, anime_here = an_anime) ##reviews = review_on_this) # reviews portion is sus

## ADD REVIEW ##


@app.route('/add_review', methods=['POST'])
def add_review():
    if 'new_user_id' not in session:
        return redirect('/')
    anime_id = request.form.get('anime_id')
    user_id = session['new_user_id']
    review_text = request.form.get('review_of_anime')
    if not anime_id or not review_text:
        flash('Invalid data. Please provide both anime ID and review.')
        return redirect(request.referrer)
    # Call the add_anime_review method to add the review
    result = Animes.add_anime_review(anime_id, user_id, review_text)
    if result:
        flash('Review posted')
    else:
        flash('Failed to add the review.')
    # print('this hwaun see!?--->',review_text)
    return redirect(request.referrer)
## from gpt ^^


## EDIT ##
@app.route('/anime/edit/<int:id>', methods = ['POST','GET'])
def edit_this_anime(id):
    if request.method == 'GET':
        anime = Animes.get_anime_by_id(id)
        return render_template('edit_anime.html', this_anime = anime)
    if not Animes.validate_anime_entry(request.form):
        return redirect(f'/anime/edit/{id}')
    anime = Animes.edit_anime_by_id(request.form)
    return redirect('/user/profile')

## DELETE ##
@app.route('/anime/delete/<int:id>')
def delete_anime_by_id(id):
    Animes.delete_anime(id)
    return redirect('/user/profile')