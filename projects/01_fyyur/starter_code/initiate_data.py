from os import stat
from unicodedata import name
from app import db, app, Show , session, Artist, Venue, Area

app.app_context().push()

artist1 = Artist(
    name = 'Taylor Swift',
    image_link = 'https://media1.popsugar-assets.com/files/thumbor/0ebv7kCHr0T-_O3RfQuBoYmUg1k/475x60:1974x1559/fit-in/500x500/filters:format_auto-!!-:strip_icc-!!-/2019/09/09/023/n/1922398/9f849ffa5d76e13d154137.01128738_/i/Taylor-Swift.jpg'
) 
artist2 = Artist(
    name = 'Ed Sheeran',
    image_link = 'https://m.media-amazon.com/images/M/MV5BODI4NTkxOTkxMV5BMl5BanBnXkFtZTgwMzE0MDEzMTE@._V1_UY1200_CR85,0,630,1200_AL_.jpg'
) 

artist3 = Artist(
    name = 'Lady Gaga',
    image_link = 'https://pbs.twimg.com/media/Fba04QZakAc6rBH.jpg'
) 

artist4 = Artist(
    name = 'Passanger',
    image_link = 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Passenger-1983.jpg/1200px-Passenger-1983.jpg'
) 

area1 = Area(
    city = 'Vancouver',
    state = 'BC'
)
area2 = Area(
    city = 'Calgary',
    state = 'AB'
)
area3 = Area(
    city = 'Seatle',
    state = 'WA'
)

show1 = Show(
    artist_id = 1,
    venue_id = 1, 
   start_time = '2022-08-09 22:00'
)
db.session.add(area1)
db.session.add(area2)
db.session.add(area3)

db.session.add(artist1)
db.session.add(artist2)
db.session.add(artist3)
db.session.add(artist4)

db.session.add(show1)
db.session.commit()