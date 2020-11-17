# CREATE TABLE album ("id" integer primary key autoincrement, "year" integer, "artist" text,"genre" text,"album" text);
# CREATE TABLE sqlite_sequence(name,seq);
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bottle import HTTPError

DB = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    engine = sa.create_engine(DB)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def create(new_album):
    #Функция принимает на вход словарь и записывает информацию из него в базу данных об альбомах.
    session = connect_db()

    #Проверяю, есть ли в базе альбом с таким же названием, при первой же встрече функция заканчивает свою работу, взовращая единицу.
    for value in session.query(Album).filter(Album.album == new_album["album"]):
        return 1

    album = Album(year=new_album["year"], artist=new_album["artist"], genre=new_album["genre"], album=new_album["album"])
    session.add(album)
    session.commit()
    #Вывожу в консоль сообщение о создании нового альбома.
    print("Добавлен альбом " + new_album["album"])

def finder(artist_name):
    #Функция принимает на вход имя артиста и возвращает словарь вида: {*Номер в порядке записи в БД*: "Название Альбома" ...}  
    session = connect_db()
    albums = session.query(Album)

    him_albums = {}
    i = 0

    for album1 in albums.filter(Album.artist == artist_name):
        i+=1
        him_albums[i] = album1.album
    return him_albums