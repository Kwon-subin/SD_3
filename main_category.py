from flask import Blueprint, render_template, request, session


bp_class = Blueprint('class', __name__)


@bp_class.route('/main_class')
def main_class():
    return render_template("main_class.html")

@bp_class.route('/art')
def art():
    return render_template("class_category_art.html")

@bp_class.route('/beauty')
def beauty():
    return render_template("class_category_beauty.html")

@bp_class.route('/cooking')
def cooking():
    return render_template("class_category_cooking.html")

@bp_class.route('/experience')
def experience():
    return render_template("class_category_experience.html")


@bp_class.route('/experience/craft')
def experience_craft():
    return render_template("class_show.html",data = '/experience/craft', teacher = session['T'],
        b_category = 'experience', s_category='craft')
@bp_class.route('/experience/dance_vocal')
def experience_dance_vocal():
    return render_template("class_show.html",data= '/experience/dance_vocal', teacher = session['T'],
        b_category = 'experience', s_category='dance_vocal')
@bp_class.route('/experience/flower')
def experience_flower():
    return render_template("class_show.html",data='/experience/flower', teacher = session['T'],
        b_category = 'experience', s_category='flower')
@bp_class.route('/experience/etc')
def experience_etc():
    return render_template("class_show.html",data='/experience/etc', teacher = session['T'],
        b_category = 'experience', s_category='etc')


@bp_class.route('/beauty/cosmetic')
def beauty_cosmetic():
    return render_template("class_show.html",data='/beauty/cosmetic', teacher = session['T'],
        b_category = 'beauty', s_category='cosmetic')
@bp_class.route('/beauty/soap')
def beauty_soap():
    return render_template("class_show.html",data='/beauty/soap', teacher = session['T'],
        b_category = 'beauty', s_category='soap')
@bp_class.route('/beauty/perfume')
def beauty_perfume():
    return render_template("class_show.html",data='/beauty/perfume', teacher = session['T'],
        b_category = 'beauty', s_category='perfume')
@bp_class.route('/beauty/etc')
def beauty_etc():
    return render_template("class_show.html",data='/beauty/etc', teacher = session['T'],
        b_category = 'beauty', s_category='etc')


@bp_class.route('/cooking/baking')
def cooking_baking():
    return render_template("class_show.html",data='/cooking/baking', teacher = session['T'],
        b_category = 'cooking', s_category='baking')
@bp_class.route('/cooking/drink')
def cooking_drink():
    return render_template("class_show.html",data='/cooking/drink', teacher = session['T'],
        b_category = 'cooking', s_category='drink')
@bp_class.route('/cooking/meal')
def cooking_meal():
    return render_template("class_show.html",data='/cooking/meal', teacher = session['T'],
        b_category = 'cooking', s_category='meal')
@bp_class.route('/cooking/etc')
def cooking_etc():
    return render_template("class_show.html",data='/cooking/etc', teacher = session['T'],
        b_category = 'cooking', s_category='etc')


@bp_class.route('/art/handwriting')
def art_handwriting():
    return render_template("class_show.html",data='/art/handwriting', teacher = session['T'],
        b_category = 'art', s_category='handwriting')
@bp_class.route('/art/drawing')
def art_drawing():
    return render_template("class_show.html",data='/art/drawing', teacher = session['T'],
        b_category = 'art', s_category='drawing')
@bp_class.route('/art/coloring')
def art_coloring():
    return render_template("class_show.html",data='/art/coloring', teacher = session['T'],
        b_category = 'art', s_category='coloring')
@bp_class.route('/art/etc')
def art_etc():
    return render_template("class_show.html",data='/art/etc', teacher = session['T'],
        b_category = 'art', s_category='etc')