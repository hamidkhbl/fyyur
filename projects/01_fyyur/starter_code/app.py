#region Import
import json
from json import JSONEncoder
from os import stat
from unicodedata import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import select
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship
import datetime
import pytz

utc=pytz.UTC
#endregion


#region AppConfig

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
# 1. Created a Postgresql (createdb fuyyurdb)
# 2. Run "flask db init", "flask db migrate" and "flask db upgrade"
migrate = Migrate(app, db)
Base = declarative_base()
#endregion  

#region Helper
def format_datetime(value, format='medium'):
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
        date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime
#endregion

@app.route('/')
def index():
  return render_template('pages/home.html')


#region Venue ----------------------------------------------------------------------
class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref = db.backref('venue_show'))
    
    def __repr__(self):
      return self.name
    
@app.route('/venues')
def venues():
  
  areas = Venue.query.distinct(Venue.city, Venue.state).all()
  venues = Venue.query.all()
  data = []
  for area in areas:
    d = {}
    venue_list = []
    d['city'] = area.city
    d['state'] = area.state
    for venue in venues:
      if venue.city == area.city and venue.state == area.state:
        venue_list.append(venue)
    d['venues'] = venue_list
    data.append(d)
        
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": Venue.query.filter(Venue.name.contains(request.form['search_term'])).count(),
    "data": Venue.query.filter(Venue.name.contains(request.form['search_term'])).all()
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  now = utc.localize(datetime.datetime.utcnow())
  data = Venue.query.filter_by(id = venue_id).one()
  return render_template('pages/show_venue.html', venue=data, now=now)

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  try:
    seeking_talent_value = (True if str(request.form['seeking_talent'])=='y' else False)
  except:
    seeking_talent_value = False
  
  try:
    venue = Venue(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      address = request.form['address'],
      phone = request.form['phone'],
      image_link = request.form['image_link'],
      facebook_link = request.form['facebook_link'],
      website_link = request.form['website_link'],
      seeking_talent = seeking_talent_value,
      seeking_description = request.form['seeking_description']
    )
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    db.session.rollback()
    flash('An error occurred. Venue '+request.form['name']+' could not be listed.' + str(e), 'error')
  finally:
    db.session.close()
    
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  
  print("Deleting...")
  try:
    venue = Venue.query.filter_by(id = venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('Venue ' + request.form['name'] + ' cannot be deleted!')
  finally:
    db.session.close()
    
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id = venue_id).one()
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    seeking_talent_value = (True if str(request.form['seeking_talent'])=='y' else False)
  except:
    seeking_talent_value = False
  try:
    venue = Venue.query.filter_by(id = venue_id).one()
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website_link = request.form['website_link']
    venue.image_link = request.form['image_link']
    venue.seeking_talent = seeking_talent_value
    venue.seeking_description = request.form['seeking_description']
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully edited!')
  except Exception as e:
    db.session.rollback()
    flash('Something went wrong! Venue ' + request.form['name'] + ' was not edited!')
    print(e)
  finally:
    db.session.close()
    
  return redirect(url_for('show_venue', venue_id=venue_id))

#endregion

#region Artist----------------------------------------------------------------------

class Genre(db.Model):
  __tablename__ = 'Genre'
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(30), nullable=False)
  describe = db.Column(db.String(500), nullable = True)
  
  def __repr__(self):
      return self.title

Artist_Genre = db.Table(
  "Artist_Genre",
  db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
  db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_for_venues = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref = db.backref('artist_show'))
    def __repr__(self):
      return self.name
    
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  response={
    "count": Artist.query.filter(Artist.name.contains(request.form['search_term'])).count(),
    "data": Artist.query.filter(Artist.name.contains(request.form['search_term'])).all()
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  now = utc.localize(datetime.datetime.utcnow())
  data = Artist.query.filter_by(id=artist_id).one()
  return render_template('pages/show_artist.html', artist=data, now=now)

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist= Artist.query.filter_by(id = artist_id).one()
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    looking_for_venues = (True if str(request.form['seeking_venue'])=='y' else False)
  except:
    looking_for_venues = False
  try:
    artist= Artist.query.filter_by(id = artist_id).one()
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.website_link = request.form['website_link']
    artist.looking_for_venues = looking_for_venues
    artist.seeking_description = request.form['seeking_description']
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully edited!')
  except Exception as e:
    db.session.rollback()
    print(str(e))
    flash('Something went wrong! '+ str(e), 'error')
  

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    looking_for_venues = (True if str(request.form['seeking_venue'])=='y' else False)
  except:
    looking_for_venues = False
  try:
    artist = Artist(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      phone = request.form['phone'],
      image_link = request.form['image_link'],
      facebook_link = request.form['facebook_link'],
      website_link = request.form['website_link'],
      looking_for_venues = looking_for_venues,
      seeking_description = request.form['seeking_description']
    )
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    db.session.rollback()
    print(str(e))
    flash('Something went wrong! '+ str(e), 'error')
  finally:
    db.session.close()
    
  return render_template('pages/home.html')

#endregion

#region Show------------------------------------------------------------------------

class Show(db.Model, JSONEncoder):
  __tablename__='Show'
  id= db.Column(db.Integer, primary_key= True)
  artist_id = db.Column(db.Integer, ForeignKey('Artist.id'), nullable = False)
  venue_id = db.Column(db.Integer, ForeignKey('Venue.id'), nullable = False)
  start_time = db.Column(db.DateTime(timezone=True), nullable= False)
  artist = db.relationship('Artist', backref = db.backref('artist_show'))
  venue = db.relationship('Venue', backref = db.backref('venue_show'))
  
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = Show.query\
  .join(Artist, Artist.id == Show.artist_id)\
    .join(Venue, Venue.id == Show.venue_id).all()
  print(data)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  show = Show(
    artist_id = request.form['artist_id'],
    venue_id = request.form['venue_id'],
    start_time = request.form['start_time']
  )
  db.session.add(show)
  db.session.commit()
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
#endregion

#region Error-----------------------------------------------------------------------
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
  
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
#endregion

#region Launch----------------------------------------------------------------------
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
#endregion

