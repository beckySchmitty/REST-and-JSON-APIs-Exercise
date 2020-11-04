from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, Cupcake
from forms import CupcakeForm

app = Flask(__name__)

# connect to specific database in postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "key9876"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_home():
    form = CupcakeForm()
    return render_template('home.html', form=form)


# GET all cupcakes
@app.route('/api/cupcakes')
def list_cupcakes():
    """return data on all cupcakes in db"""
    cupcakes = Cupcake.query.all()
    response = [cp.serialize() for cp in cupcakes]
    return jsonify(cupcakes=response)

# GET specific cupcake
@app.route('/api/cupcakes/<int:cp_id>')
def show_cupcake(cp_id):
    """return data on specific cupcake"""
    cupcake = Cupcake.query.get_or_404(cp_id)
    response = cupcake.serialize()
    return (jsonify(cupcake=response), 200)

# POST cupcakeee
@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """add cupcake, return data about new cupcake"""
    form = CupcakeForm()

    # If post & form data valid
    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data

        # create cupcake with form data
        cupcake = Cupcake(
        flavor=flavor,
        rating=rating,
        size=size,
        image=(image or None))

        # add to db
        db.session.add(cupcake)
        db.session.commit()

        # return (jsonify(cupcake=cupcake.serialize()), 201)
        return redirect('/')


    else:
        return redirect('/')

#PATCH and update a specific cupcake
@app.route('/api/cupcakes/<int:cp_id>', methods=["PATCH"])
def update_cupcake(cp_id):
    """update cupcake"""
    cupcake = Cupcake.query.get_or_404(cp_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 200)

# DELETE 
@app.route('/api/cupcakes/<int:cp_id>', methods=["DELETE"])
def delete_cupcake(cp_id):

    cupcake = Cupcake.query.get_or_404(cp_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
