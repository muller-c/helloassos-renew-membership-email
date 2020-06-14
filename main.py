import datetime
import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector
import requests
import configparser
config = configparser.ConfigParser()
config.read('configuration.ini')

host = config['DB']['host']
user = config['DB']['user']
password = config['DB']['password']
database = config['DB']['database']
class Adherant:
    def __init__(self, firstname, lastname, email, date_inscription):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.date_inscription = date_inscription


class Association:
    def __init__(self, client_id, client_secret, association, campagne, login_email, password_email, server_email,
                 server_email_port, email_template, list_adherant):
        self.client_id = client_id
        self.client_secret = client_secret
        self.association = association
        self.campagne = campagne
        self.login_email = login_email
        self.password_email = password_email
        self.server_email = server_email
        self.server_email_port = server_email_port
        self.email_template = email_template
        self.list_adherant = list_adherant


def get_assocations():
    associations = []
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM association")
    myresult = mycursor.fetchall()

    for asso in myresult:
        associations.append(
            Association(asso[1], asso[2], asso[3], asso[4], asso[5], asso[6], asso[7], asso[8], asso[9], []))

    return associations


def get_adherant_details(itemid, access_token):
    url = "https://api.helloasso.com/v5/items/" + str(itemid) + "?withDetails=true"
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    datas = json.loads(response.text)

    adherant = Adherant(None,None,None,None)
    adherant.email = datas['payer']['email']
    adherant.firstname = datas['user']['firstName']
    adherant.lastname = datas['user']['lastName']
    adherant.date_inscription = datetime.datetime.strptime(datas['order']['date'].split("T")[0], '%Y-%m-%d')
    return adherant


def get_helloassos_token():
    url = "https://api.helloasso.com/oauth2/token"
    payload = 'client_id=' + association.client_id + '&client_secret=' + association.client_secret + '&grant_type=client_credentials'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    access_token = json.loads(response.text)['access_token']

    return access_token


def get_adherant(association):
    url = "https://api.helloasso.com/v5/organizations/" + association.association + "/forms/Membership/" + association.campagne + "/payments?pageIndex=1&pageSize=200000&retrieveOfflineDonations=false"
    payload = {}
    access_token = get_helloassos_token()
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    datas = json.loads(response.text)
    for items in datas["data"]:
        for item in items['items']:
            association.list_adherant.append(get_adherant_details(item['id'], access_token))


def send_email(association, adherant):
    # me == my email address
    # you == recipient's email address
    me = association.login_email
    you = adherant.email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Renouvellement"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = association.email_template

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(association.server_email, association.server_email_port, context=context) as server:
        server.login(association.login_email, association.password_email)
        server.sendmail(me, you, msg.as_string())

    # TODO: Send email here


###MAIN######
associations = []
associations = get_assocations()
for association in associations:
    get_adherant(association)
    count = 0
    for adherant in association.list_adherant:
        print("Count :"+str(count))
        print(adherant.firstname)
        print(adherant.lastname)
        print(adherant.date_inscription)
        count= count+1

# for association in associations:
#    send_email(association,Adherant("Camille","Muller","muller_camille@icloud.com",None))

#
