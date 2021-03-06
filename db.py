import sqlite3
import bcrypt
import os


def registerUser(conn, user):
    password = user['password']
    user['active'] = 0
    user['password'] = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    try:
        conn.execute(
            "INSERT INTO user (name, email, password, type, active) VALUES (:name, :email, :password, :usertype, :active)", user)
        conn.commit()
        return 1
    except sqlite3.IntegrityError:
        return 2
    except Exception:
        print "user registration exception"
        return 3


def resetUserPassword(conn, user):
    try:
        password = user['password']
        user['password'] = bcrypt.hashpw(
            password.encode('utf8'), bcrypt.gensalt())
        conn.execute(
            "UPDATE user set password = :password WHERE id= :id", user)
        return True
    except:
        return False


def checkPassword(conn, email, password):
    try:
        hashPW = conn.execute(
            "SELECT password FROM user WHERE email=?", (email,)).fetchone()
        if bcrypt.checkpw(password.encode('utf8'), hashPW[0].encode('utf8')):
            usertype = conn.execute(
                "SELECT id, type, name, active, email FROM user WHERE email=?", (email,)).fetchone()
            return usertype
        else:
            return False
    except:
        return False


def createAd(conn, ad):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO advertisements (title, description, datetime, active, user_id) VALUES (:title, :desc, :datetime, :active, :userid)", ad)
        for x in ad["imgpath"]:
            conn.execute(
                "INSERT INTO advertisement_img (path, ad_id) VALUES (?, ?)", (x, cursor.lastrowid))
        conn.commit()
        return True
    except:
        return False


def getAds(conn, search):
    ads = []
    cursor = conn.execute(
        "SELECT id, title, description, datetime, user_id FROM advertisements WHERE title LIKE ?", (search,))
    for row in cursor:
        ad = {}
        ad["id"] = row[0]
        ad["title"] = row[1]
        ad["desc"] = row[2]
        ad["datetime"] = row[3]
        ad["user_id"] = int(row[4])
        try:
            imgpath = conn.execute(
                "SELECT path FROM advertisement_img WHERE ad_id=?", (row[0],))
            ad["img_path"] = imgpath.fetchone()[0]
        except:
            ad["img_path"] = ""
        ads.append(ad)
    return ads


def deleteAds(conn, id):
    try:
        conn.execute(
            "DELETE FROM advertisements WHERE id=?", (id,)
        )
        cursor = conn.execute(
            "SELECT path FROM advertisement_img WHERE ad_id=?", (id,))
        for x in cursor:
            os.remove(x[0])
        conn.execute(
            "DELETE FROM advertisement_img WHERE ad_id=?", (id,)
        )
        conn.commit()
        return True
    except:
        return False


def editAd(conn, ad):
    conn.execute(
        "UPDATE advertisements set title = :title, description = :desc WHERE id =:id", ad
    )
    conn.commit()


def createBooking(conn, booking):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (title, description, datetime, active, location, user_id) VALUES (:title, :desc, :datetime, :active, :location, :user_id)", booking)
        conn.commit()
        return True
    except:
        return False


def getUser(conn, id):
    try:
        user = conn.execute(
            "SELECT name, email, type FROM user WHERE id=?", (id,)
        ).fetchone()
        return user
    except:
        return False


def editUser(conn, user):
    try:
        conn.execute(
            "UPDATE user set name = :name, email = :email, type = :usertype WHERE id= :id", user)
        # conn.commit()
        return True
    except:
        return False


def getUserAds(conn, userid):
    ads = []
    cursor = conn.execute(
        "SELECT id, title, description, datetime, user_id FROM advertisements WHERE user_id=?", (
            userid,)
    )
    for row in cursor:
        ad = {}
        ad["id"] = row[0]
        ad["title"] = row[1]
        ad["desc"] = row[2]
        ad["datetime"] = row[3]
        ad["user_id"] = row[4]
        try:
            imgpath = conn.execute(
                "SELECT path FROM advertisement_img WHERE ad_id=?", (row[0],))
            ad["img_path"] = imgpath.fetchone()[0]
        except:
            ad["img_path"] = ""
        ads.append(ad)
    return ads


def viewAd(conn, id):
    ads = []
    cursor = conn.execute(
        "SELECT id, title, description, datetime, user_id FROM advertisements WHERE id=?", (
            id,)
    )
    for row in cursor:
        ad = {}
        ad["id"] = row[0]
        ad["title"] = row[1]
        ad["desc"] = row[2]
        ad["datetime"] = row[3]
        ad["user_id"] = int(row[4])
        try:
            imgpath = conn.execute(
                "SELECT path FROM advertisement_img WHERE ad_id=?", (row[0],))
            ad["img_path"] = imgpath.fetchone()[0]
        except:
            ad["img_path"] = ""
        ads.append(ad)
    return ads


def getCharities(conn, sType):
    try:
        charities = conn.execute(
            "SELECT id, name, email FROM user WHERE type=?", (sType,)).fetchall()
        return charities
    except:
        return False


def getFilteredCharities(conn, searchQuery, sType):
    print searchQuery
    query = "%" + searchQuery + "%"
    try:
        charities = conn.execute(
            "SELECT id, name, email FROM user WHERE type=? AND name LIKE ?", (sType, query,)).fetchall()
        print charities
        return charities
    except:
        return False
    
def confirmUser(conn, email):
    cursor = conn.execute(
    "UPDATE user  set active =? WHERE email=?", (1, email)
    )
    return 1

def getAppointments(conn, userid):
    apps = []
    cursor = conn.execute(
        "SELECT id, title, description, datetime, location FROM bookings WHERE user_id=?", (userid,)
    )
    for row in cursor:
        print row
        ad = {}
        ad["id"] = row[0]
        ad["title"] = row[1]
        ad["desc"] = row[2]
        ad["datetime"] = row[3]
        ad["location"] = row[4]
        apps.append(ad)
        print ad
    if len(apps) == 0:
        print "no appointments"
    return apps
def editApp(conn, app):
    conn.execute(
        "UPDATE bookings set title = :title, description = :desc, datetime = :datetime, location = :location WHERE id =:id", app
    )
    conn.commit()

def deleteApp(conn, id):
    try:
        conn.execute(
            "DELETE FROM bookings WHERE id=?", (id,)
        )
        conn.commit()
        return True
    except:
        return False