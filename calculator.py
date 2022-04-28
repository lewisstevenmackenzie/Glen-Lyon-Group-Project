# 4 steps to the journey calculation
# step 1: countries lorry co2 * distance * weight
# step 2: shipping cost * weight
# step 3: uk lorry cost * distance * weight
# step 4: add the three variables together to get the total carbon emission 

from coffeeCalc.models import Country

def co2_cost(weight, origin_to_port, start_country, port_to_client):
    
    # query the database for the port/countries information
    origin_country = Country.query.filter_by(title = start_country).all()

    # step 1: get co2 emissions for origin countries lorry
    origin_co2 = origin_country[0].region_to_port_cost

    # step 2: get co2 for the shipping container 
    shipping_co2 = origin_country[0].port_to_UK_cost 

    # step 3: uk lorry co2
    uk_co2 = 0.0000761

    # step 4: total co2
    total_co2 = ((float(weight) * float(origin_co2) * float(origin_to_port)) + (float(weight) * float(shipping_co2)) + (float(weight) * float(port_to_client)*uk_co2))
    return total_co2