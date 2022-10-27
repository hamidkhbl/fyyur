from app import db, app, Show , session, Artist, Venue, Area

app.app_context().push()

show = Show(
    artist_id = 1,
    venue_id = 1, 
    start_time = '2022-08-09 22:00'
)

db.session.add(show)
db.session.commit()


data = Show.query.all()
data1 = Area.query.all()
print(data)
print('done')