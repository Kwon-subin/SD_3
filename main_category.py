import ESGuide as es
from flask import Blueprint, render_template, request, session


bp_class = Blueprint('class', __name__)


def getClasses(ctgry_name, ctgry_detail):
        ctgry = es.get_doc('category', ctgry_name)
        print(ctgry)
        class_ids_ = ctgry['_source']['detail']
        class_ids = None
        for class_ids in class_ids_:
            if class_ids['name'] == ctgry_detail:
                break
        class_ids = class_ids['class']

        if len(class_ids) == 0:
            return []
        
        classes = es.get_docs('class', class_ids)

        return classes


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
    classes = getClasses('experience', 'craft')
    return render_template("class_list.html",data = '/experience/craft', teacher = session['T'],
        b_category = 'experience', s_category='craft', reading = classes)

@bp_class.route('/experience/dance_vocal')
def experience_dance_vocal():
    classes = getClasses('experience', 'dance_vocal')
    return render_template("class_list.html",data= '/experience/dance_vocal', teacher = session['T'],
        b_category = 'experience', s_category='dance_vocal', reading = classes)

@bp_class.route('/experience/flower')
def experience_flower():
    classes = getClasses('experience', 'flower')
    return render_template("class_list.html",data='/experience/flower', teacher = session['T'],
        b_category = 'experience', s_category='flower', reading = classes)

@bp_class.route('/experience/etc')
def experience_etc():
    classes = getClasses('experience', 'etc')
    return render_template("class_list.html",data='/experience/etc', teacher = session['T'],
        b_category = 'experience', s_category='etc', reading = classes)




@bp_class.route('/beauty/cosmetic')
def beauty_cosmetic():
    classes = getClasses('beauty', 'cosmetic')
    return render_template("class_list.html",data='/beauty/cosmetic', teacher = session['T'],
        b_category = 'beauty', s_category='cosmetic', reading = classes)

@bp_class.route('/beauty/soap')
def beauty_soap():
    classes = getClasses('beauty', 'soap')
    return render_template("class_list.html",data='/beauty/soap', teacher = session['T'],
        b_category = 'beauty', s_category='soap', reading = classes)
        
@bp_class.route('/beauty/perfume')
def beauty_perfume():
    classes = getClasses('beauty', 'perfume')
    return render_template("class_list.html",data='/beauty/perfume', teacher = session['T'],
        b_category = 'beauty', s_category='perfume', reading = classes)

@bp_class.route('/beauty/etc')
def beauty_etc():
    classes = getClasses('beauty', 'etc')
    return render_template("class_list.html",data='/beauty/etc', teacher = session['T'],
        b_category = 'beauty', s_category='etc', reading = classes)




@bp_class.route('/cooking/baking')
def cooking_baking():
    classes = getClasses('cooking', 'baking')
    return render_template("class_list.html",data='/cooking/baking', teacher = session['T'],
        b_category = 'cooking', s_category='baking', reading = classes)

@bp_class.route('/cooking/drink')
def cooking_drink():
    classes = getClasses('cooking', 'drink')
    return render_template("class_list.html",data='/cooking/drink', teacher = session['T'],
        b_category = 'cooking', s_category='drink', reading = classes)

@bp_class.route('/cooking/meal')
def cooking_meal():
    classes = getClasses('cooking', 'meal')
    return render_template("class_list.html",data='/cooking/meal', teacher = session['T'],
        b_category = 'cooking', s_category='meal', reading = classes)

@bp_class.route('/cooking/etc')
def cooking_etc():
    classes = getClasses('cooking', 'etc')
    return render_template("class_list.html",data='/cooking/etc', teacher = session['T'],
        b_category = 'cooking', s_category='etc', reading = classes)




@bp_class.route('/art/handwriting')
def art_handwriting():
    classes = getClasses('art', 'handwriting')
    return render_template("class_list.html",data='/art/handwriting', teacher = session['T'],
        b_category = 'art', s_category='handwriting', reading = classes)

@bp_class.route('/art/drawing')
def art_drawing():
    classes = getClasses('art', 'drawing')
    return render_template("class_list.html",data='/art/drawing', teacher = session['T'],
        b_category = 'art', s_category='drawing', reading = classes)

@bp_class.route('/art/coloring')
def art_coloring():
    classes = getClasses('art', 'coloring')
    return render_template("class_list.html",data='/art/coloring', teacher = session['T'],
        b_category = 'art', s_category='coloring', reading = classes)

@bp_class.route('/art/etc')
def art_etc():
    classes = getClasses('art', 'etc')
    return render_template("class_list.html",data='/art/etc', teacher = session['T'],
        b_category = 'art', s_category='etc', reading = classes)