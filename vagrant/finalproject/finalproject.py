from flask import Flask

app= Flask(__name__)


##############################################
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return "this page will show all restaurants"

@app.route('/restaurants/new')
def newRestaurant():
    return "this page will create a new restaturent"

@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return "this page will be for editing restaurant %s"%restaurant_id

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    return "this pagae to delete restaurant %s" %restaurant_id

#############################################
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
    return 'this page will show menus of a restauratn %s '%restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    return'This will create a new menu item for restaurant %s'%restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id,menu_id):
    return " this will edit menu item %s" %menu_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id,menu_id):
    return " this will delete menu item %s" %menu_id
####################



if __name__=='__main__':
    app.secret_key= 'super_secret_key'
    app.debug=True
    app.run(host='0.0.0.0', port=5000)
