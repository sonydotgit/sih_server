from flask import Flask, request, jsonify, send_from_directory
import db
import psycopg2 as psyco

app = Flask(__name__)

@app.route('/gramRule', methods=['POST', 'GET'])
def gramRule():
    """Get Rule JSON"""
    """Receive:
            - gramPanchayatID
       Send:
            - rules(json)
    """
    user_dict = request.get_json()

    # ESTABLISH DB CONNECTION ############## 
    conn = db.connect_db()
    if conn == None:
        return "Error Connecting to db", 500

    cur = conn.cursor()

    # Query
    get_jrule_q = """
                  SELECT j_rules
                  From GramPanchayat
                  WHERE gram_id=%s"""
    cur.execute(get_jrule_q, (user_dict['gramPanchayatID'],))

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return "No data found", 404

    jruleo = []

    for jrule in cur.fetchall():
        jruleo.append(jrule)

    print(jruleo)

    return jruleo, 200

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

@app.route('/putpdetails', methods=['GET', 'POST'])
def pdetails():
    """
        Receives:
            - project_id
            - client_id
            - gram_id
            - eng_email
            - Docs [Aadhar, property, dwg]
        Sends:
            - Success Response
    """

    # ESTABLISH DB CONNECTION ############## 
    conn = db.connect_db()
    if conn == None:
        return "Error Connecting to db", 505

    cur = conn.cursor()

    user_dict = request.get_json()

    # Query to insert
    p_ins_q = """
              INSERT INTO Project
              (project_id, cli_id, eng_id, gram_id)
              VALUES
              (%s, %s, %s, %s)
              """

    pid = user_dict['project_id']
    user_dict['project_id'] = pid[:10]

    try:
        cur.execute(p_ins_q, (user_dict['project_id'],
                              user_dict['client_id'],
                              user_dict['eng_email'],
                              user_dict['gram_id']
        ))
        return "Insertion Done", 200
    except (Exception, psyco.DatabaseError) as e:
        print(e)
        cur.close()
        conn.close()
        return "Error while inserting", 500

##################################################

@app.route('/getpdetails', methods=['GET', 'POST'])
def getpdetails():
    """Send Client details"""
    """Receives:
            - 
       Sends:
            - project_id
            - client_id
            - eng_email
            - gram_id
    """

    # ESTABLISH DB CONNECTION ############## 
    conn = db.connect_db()
    if conn == None:
        return "Error Connecting to db", 500
    cur = conn.cursor()

    user_dict = request.get_json()

    # Query
    get_p_q = """
              SELECT project_id, client_id, eng_id, gram_id
              FROM Project
              """
    cur.execute(get_p_q)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return "No data found", 404

    finalList = {'project':[]}

    for pid, cid, eemail, gid in cur.fetchall():
        finalList['client'].append({
            'client_id': cid,
            'eng_email': eemail,
            'gram_id': gid,
            'project_id': pid
            })

    return jsonify(finalList), 200

@app.route('/updateStatus', methods=['GET', 'POST'])
def updateStatus():
    """Update project status"""
    """Receives:
            - project_id
            - emp_id
            - assign_date
            - p_step
       Sends:
            - Push notification to all devices
    """

    # ESTABLISH DB CONNECTION ############## 
    conn = db.connect_db()
    if conn == None:
        return "Error Connecting to db", 500
    cur = conn.cursor()

    user_dict = request.get_json()

    # Query
    up_stat_q = """INSERT INTO ProjectStatus
                   (project_id, emp_id, assign_date, p_step)
                   VALUES
                   (%s, %s, %s, %s)
                """
    try:
        cur.execute(up_stat_q, (user_dict['project_id'],
                                user_dict['emp_id'],
                                user_dict['assign_date'],
                                user_dict['p_step']
        ))
        notify = Notify()
        message = user_dict['project_id'] + ': ' + user_dict['p_step']
        notify.send(message)
        return "Updating completed", 200
    except (Exception, psyco.DatabaseError) as e:
        print(e)
        return "Failed to update status", 500
        
@app.route('/getEng', methods=['POST', 'GET'])
def getEng():
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

@app.route('/getClients', methods=['GET','POST'])
def getClients():
    """Get clients"""
    """Receives:
            - clientEmail
       Sends:
            - clientId
            - clientAadhar
            - clientName
            - clientAddress
            - clientMobile
            - clientEmail
    """

    user_dict = request.get_json()

    # ESTABLISH DB CONNECTION ############## 
    conn = db.connect_db()
    if conn == None:
        return "Error Connecting to db", 500

    cur = conn.cursor()

    # Get clients query
    get_client_q = """
                   SELECT cli_id, cli_aadhar, cli_name, cli_address,
                   cli_mobile, cli_email
                   FROM Client
                   WHERE cli_email=%s
                   """
    cur.execute(get_client_q, (user_dict['clientEmail'],))
    
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return "No data found", 404

    finalList = {'client':[]}

    for clientId, clientAadhar, clientName, clientAddress, clientMobile, clientEmail in cur.fetchall():
        finalList['client'].append({
            'clientId': clientId, 
            'clientAadhar': clientAadhar,
            'clientName': clientName,
            'clientAddress': clientAddress,
            'clientMobile': clientMobile,
            'clientEmail': clientEmail})

    return jsonify(finalList), 200

if __name__ == '__main__':
    app.run()
