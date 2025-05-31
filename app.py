import datetime
import os
from flask import Flask, render_template,request
from pymongo import MongoClient
from dotenv import load_dotenv
  
load_dotenv()

def create_app():
    app=Flask(__name__)
    client= MongoClient(os.getenv("MONGODB_URL")) #MongoClient as a cluster representation
    app.db= client.microblog    #client.database actually connects to the database and is stored in app

#entries=[]  temporary list to store entries coming from web page 

    @app.route("/",methods=["GET","POST"])
    def home():
    #print([e for e in app.db.entries.find({})])
        if request.method=="POST":
            entry_content = request.form.get("content")
            formatted_date=datetime.datetime.today().strftime("%Y-%m-%d")
            #entries.append((entry_content,formatted_date))
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html",entries=entries_with_date) # entries variable is created in the template that will contain list of tuples
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
# .\.venv\Scripts\activate
#python app.py


