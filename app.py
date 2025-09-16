from flask import Flask,request,jsonify
import psycopg2
import os 

app = Flask(__name__)
#connect to the database
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "votes"),
        user=os.getenv("DB_USER" , "postgres"),
        password=os.getenv("DB_PASSWORD" , "postgres")
    )
    return conn


#write to the database
@app.route("/vote", methods =["POST"])
def vote():
    data = request.json
    choice=data.get("choice")

    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute("INSERT INTO votes (choice) VALUES (%s)" , (choice,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message":"Vote recorded ! "})

#read from the database
@app.route("/results", methods =["GET"])
def results():
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute("SELECT choice , COUNT(*) FROM votes GROUP BY choice;")
    results = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(dict(results))

if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=5000)