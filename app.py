from flask import Flask, request, jsonify, send_from_directory
import db
import psycopg2 as psyco

app = Flask(__name__)

@app.route('/getGramPans', methods=['POST','GET'])
def getGrams():
    """Get List of Gram Panchayats"""
    """Receives:
            - State
            - District
       Sends:
            - gramPanchayatName
            - gramPanchayatID
    """
    user_dict = request.get_json()

    # ESTABLISH DB CONNECTION ############## 
    conn = db.connect_db()
    if conn == None:
        return "Error Connecting to db", 500

    cur = conn.cursor()

    # Query to get g_name and g_id
    g_name_id = """SELECT gram_id, gram_name
                   FROM GramPanchayat
                   WHERE g_district=%s"""
    cur.execute(g_name_id, (user_dict["District"],))

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return "No GramPanchayats found", 404

    finalList = {'gram':[]}

    for gid, gname in cur.fetchall():
        finalList['gram'].append({'gramPanchayatName': gname, 'gramPanchayatID': gid})

    return jsonify(finalList), 200

# @app.route('/getEng', methods=['POST', 'GET'])
# def getEng():
    """Get """

if __name__ == '__main__':
    app.run()
