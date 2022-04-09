

## get database

## 3 parts to the journey

## part 1 countries lorry co2 * distance

## part 2 shipping cost * weight

## part 3 uk lorry cost * weight

from coffeeCalc import app, db, bcrypt
from coffeeCalc.forms import SignUpForm, LoginForm, PostForm, NoteForm
from coffeeCalc.models import User, Post, Note, Country

def co2_cost(weight, origin_to_port, start_country, port_to_client):
    print("test3: " + start_country)
    #origin_country = Country.query.get_or_404(title = start_country)
    origin_country = Country.query.filter_by(title = start_country).all()
    #posts =Post.query.filter_by(user_id=user_id).all()
    print("test4" + origin_country[0].title)
    origin_co2 = origin_country[0].region_to_port_cost
    #print("test5" +str(origin_co2))
    shipping_co2 = origin_country[0].port_to_UK_cost 
    #print("test6" + str(shipping_co2))
    total_co2 = ((int(weight)*int(origin_co2)*int(origin_to_port)) + (int(weight)*int(shipping_co2)) + (int(weight)*int(port_to_client)*1))
    print("test7" + str(total_co2))
    return total_co2