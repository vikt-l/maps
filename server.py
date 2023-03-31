from flask import Flask, render_template, request, redirect
from getMap import get_info, get_address, get_obj
from forms.default import DefaultForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = DefaultForm()
    if request.method == 'POST':
        if form.delta.data:
            delta = form.delta.data
        else:
            delta = 0.2
            form.delta.data = 0.2
        img = 'static/img/default_img.png'
        if form.address.data:
            address = form.address.data
            img = get_address(address, delta)
        elif form.longitude.data and form.lattitude.data:
            toponym_longitude = form.longitude.data
            toponym_lattitude = form.lattitude.data
            if form.object.data:
                object = form.object.data
                img = get_obj(toponym_longitude, toponym_lattitude, object, delta)
            else:
                img = get_info(toponym_longitude, toponym_lattitude, delta)
        return render_template('default.html', form=form, img=img)
    return render_template('default.html', form=form, img='static/img/default_img.png')


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")