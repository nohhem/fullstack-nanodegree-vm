from flask import Flask,render_template,request,redirect,url_for,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


app= Flask(__name__)

###DB connection setup##
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

##################
#mockup data
#Fake Restaurants
restaurants = {'name': 'The CRUDdy Crab', 'id': '1'}

#restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

##############################################
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    ##return "this page will show all restaurants"
    restaurants=session.query(Restaurant)

    return render_template('restaurants.html',restaurants=restaurants)

@app.route('/restaurants/newrestaurants.html', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        name= request.form['name']
        restaurant=Restaurant(name=name)
        session.add(restaurant)
        session.commit()
        flash('new restaurant added !!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')
        return "this page will create a new restaturent"


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method=='POST':
        restaurant= session.query(Restaurant).filter_by(id=restaurant_id).one()
        restaurant.name=request.form['name']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        restaurant= session.query(Restaurant).filter_by(id=restaurant_id).one()
        print restaurant,restaurant.name
        return render_template('editrestaurant.html',restaurant=restaurant)
        ##return "this page will be for editing restaurant %s"%restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        session.delete(restaurantToDelete)
        session.commit()
        flash(restaurantToDelete.name+" deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html',restaurant=restaurantToDelete)

#############################################
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id)

    for x in items: print x.name
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if not items: flash("you currently have no menu items")
    return render_template('menu.html',restaurant=restaurant,items=items)
    return 'this page will show menus of a restauratn %s '%restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method=="POST":
        menuitem=MenuItem(name=request.form['name'],description=request.form['description']
            ,price=request.form['price'],course=request.form['course'],restaurant_id=restaurant_id)
        print menuitem,menuitem.name,menuitem.price,menuitem.course,menuitem.description
        session.add(menuitem)
        session.commit()
        print menuitem

        return redirect(url_for("showMenu",restaurant_id=restaurant_id))

    else:
        return render_template('newmenuitem.html',restaurant_id=restaurant_id)

    return'This will create a new menu item for restaurant %s'%restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id,menu_id):
    if request.method=="POST":
        menuitem=session.query(MenuItem).filter_by(id=menu_id).one()
        if request.form['name']:
            menuitem.name=request.form['name']
        session.add(menuitem)
        session.commit()
        flash("the menu with id:"+str(menu_id)+" edited")
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id,menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash(" menu item Deleted!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete)
####################



if __name__=='__main__':
    app.secret_key= 'super_secret_key'
    app.debug=True
    app.run(host='0.0.0.0', port=5000)


