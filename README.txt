Coffee Supply Chain Carbon Footprint Calculation

Team: 138
PM: Robbie Mitchell
Harry Addlesee
Roan Creed
Lewis Mackenzie
Lewis Melrose
Ewan Robertson

Client: Glen Lyon Coffee Roasters

Sponsor: Frances Ryan

Brief: web application that will calculate the carbon emissions produced by transporting coffee beans from different origin farms to roasteries across the UK

Clone repository to server: 
    git clone https://github.com/lewisstevenmackenzie/Glen-Lyon-Group-Project.git

Walkthrough for hosting available at:
    https://bdavison.napier.ac.uk/web/server/apache/


Libraries to install after creating the virtual environment:
- pip install Flask
- pip install flask-wtf
- pip install email_validator
- pip install flask-sqlalchemy
- pip install flask-bcrypt
- pip install flask-login

How to Create the Databse:
Whilst in the servers git directory, run the following commands. 
- python3
- from coffeeCalc.__init__ import db
- db.create_all()

How to add a Country:
Whilst in the servers git directory, run the following commands. 
- python3
- from coffeeCalc.init import db
- from coffeeCalc.models import Country
- country1 = Country(title = "countryName", region = "regionName", port = "portName", region_to_port_cost = "decimal value", port_to_UK_cos = "decimal value")
- db.session.add(country1)
- db.session.commit()

How to host the Website:
In the myapp.wsgi file replace: 
  import sys

  sys.path.insert(0, '/usr/local/env/myApp/')

  from app.myApp import application

with: 
  import sys

  sys.path.insert(0, '/usr/local/env/myApp/')

  from coffeCalc.__init__ import application

run the following command to run the hosting:
 - sudo a2ensite myApp
 - sudo service apache2 stop
 - sudo service apache2 start

