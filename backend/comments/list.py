import os

import mysql.connector


db = os.environ["MYSQL_DB"]
pw = os.environ["MYSQL_PW"]

def handler():
  # Connect with the MySQL Server
  cnx = mysql.connector.connect(database=db, password=pw)

  # Get two buffered cursors
  curA = cnx.cursor(buffered=True)

  # Query to get employees who joined in a period defined by two dates
  query = (
    "SELECT c.comment, c.date, u.name as user_name"
    "FROM comments c"
    "LEFT JOIN users u"
    "ON comments.user_id = users.id")

  # Select the employees getting a raise
  curA.execute(query)

  records = []
  # Iterate through the result of curA
  for (comment, date, user_name) in curA:

    # Update the old and insert the new salary
    record = {"comment": comment, "date": date, "user_name": user_name}

    records.append(record)

  data = {"data": {"comments": records}}

  return data