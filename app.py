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
    """Get detail of Engineer"""
    """Receives:
            - engEmail
       Sends:
            - engAadhar
            - engName
            - engAddress
            - engMobile
            - engEmail
            - engRole
            - licenseNo
            - validUpto
    """
    user_dict = request.get_json()

    # ESTABLISH DB CONNECTION ############## 
    conn = db.connect_db()
    if conn == None:
        return "Error Connecting to db", 500

    cur = conn.cursor()

    # Query to retreive engineer
    get_eng_q = """
                SELECT eng_aadhar,
                       eng_name,
                       eng_address,
                       eng_mobile,
                       eng_email,
                       eng_role,
                       license_no,
                       valid_upto
                FROM Engineering
                WHERE eng_email=%s
                """
    cur.execute(get_eng_q, (user_dict['engEmail'],))

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return "No Data Associated to that email found", 404 

    finalList = {'eng':[]}

    for engAadhar, engName, engAddress, engMobile, engEmail, engRole, licenseNo, validUpto in cur.fetchall():
        finalList['eng'].append({'engAadhar': engAadhar,
            'engName': engName,
            'engAddress': engAddress,
            'engMobile': engMobile,
            'engEmail': engEmail,
            'engRole': engRole,
            'licenseNo': licenseNo,
            'validUpto': validUpto})

    return jsonify(finalList), 200

if __name__ == '__main__':
    app.run()
