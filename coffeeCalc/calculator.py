## 3 parts to the journey calculation

## part 1: countries lorry co2 * distance * weight

## part 2: shipping cost * weight

## part 3: uk lorry cost * distance * weight

## Finally add the three sums together to attain the total carbon emission 

from coffeeCalc import app, db, bcrypt
from coffeeCalc.forms import SignUpForm, LoginForm, PostForm, NoteForm
from coffeeCalc.models import User, Post, Note, Country

def co2_cost(weight, origin_to_port, start_country, port_to_client):
    
    # Query the database for the port/countries information
    origin_country = Country.query.filter_by(title = start_country).all()
    # Part 1: attain co2 emissions for origin countries lorry
    origin_co2 = origin_country[0].region_to_port_cost

    # Part 2: attain co2 for the shipping container 
    shipping_co2 = origin_country[0].port_to_UK_cost 

    # Part 3: uk lorry co2
    UK_co2 = 0.0000761

    # Part 4: Total co2
    total_co2 = ((float(weight)*float(origin_co2)*float(origin_to_port)) + (float(weight)*float(shipping_co2)) + (float(weight)*float(port_to_client)*UK_co2))
    return total_co2