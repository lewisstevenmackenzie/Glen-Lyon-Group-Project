

## get database

## 3 parts to the journey

## part 1 countries lorry co2 * distance

## part 2 shipping cost * weight

## part 3 uk lorry cost * weight


def co2_cost(weight, origin_to_port, start_country, port_to_client)

    origin_country = Country.query.get_or_404(start_country)
    origin_co2 = origin_country.region_to_port_cost()
    shipping_co2 = origin_country.port_to_UK_cost() 

    total_co2 = weight*origin_co2*origin_to_port + weight*shipping_co2 + weight*port_to_client*0.0000761