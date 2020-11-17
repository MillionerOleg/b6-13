# CREATE TABLE album ("id" integer primary key autoincrement, "year" integer, "artist" text,"genre" text,"album" text);
# CREATE TABLE sqlite_sequence(name,seq);
from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums", method="POST")
def albums():
    new_album = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album"),
    }
    #Обрабатываю все возможные ошибки ввода данных и возможность их отсутствия.
    try:
        int(new_album["year"])
    except ValueError:
        return HTTPError(400, "Неверное значение или отсутствие года выхода альбома.\n Примеры верного ввода: \"1991\", \"2000\", \"2020\"")
    except TypeError:
        return HTTPError(400, "Неверное значение или отсутствие года выхода альбома.\n Примеры верного ввода: \"1991\", \"2000\", \"2020\"")
    if type(new_album["artist"]) != str or type(new_album["genre"]) != str or type(new_album["album"]) != str:
        return HTTPError(400, "Неверное значение или отсутствие одного из параметров альбома.\n Для записи альбом должен содержать: Год выхода, Название группы, Жанр и Название самого альбома.")
    
    #Передаю словарь в функцию создания нового альбома.
    check = album.create(new_album)
    #Если альбом будет создан, то функция ничего не вернёт, но если в базе уже альбом с таким названием функция возвращает 1 и это приводит к ошибке 409
    if check:
        return HTTPError(409, "Альбом {} уже есть в базе".format(new_album["album"]))
    return "Добавлен альбом " + new_album["album"]

@route("/albums/<artist>")
def albums(artist):
    #Через функцию поиска получаю словаь со всеми альбомами группы. Если их нет - получаю пустой список.
    star_albums = album.finder(artist)
    #Создаю строку со всеми альбомами и их количеством, а затем возвращаю её
    res = "Найдено {} альбомов группы {}:".format(str(len(star_albums)), artist)
    for number, value in star_albums.items():
        res+="\n{}. \"{}\"".format(number, value)
    return res

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)