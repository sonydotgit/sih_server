import db, json
import psycopg2 as psyco

def insert_jRule():
    try:
        conn = db.connect_db()
        cur = conn.cursor()

        json_val = 

        insert_jrule_q = """
                         INSERT INTO GramPanchayat
                         (j_rules) VALUES (%s)
                         WHERE gram_id=%s
                         """

# conn = None
# try:
#     conn = db.connect_db()
#     cur = conn.cursor()
# 
#     commands = """
#                INSERT INTO Engineering 
#                (eng_id, eng_aadhar, eng_name, eng_address, eng_mobile,
#                 eng_email, eng_role, license_no, valid_upto
#                )
#                VALUES
#                (
#                 %s, %s,%s,  %s,  %s,  %s,  %s,  %s,  %s 
#                )
#                """
# 
#     cur.execute(commands, ("eng001",
#                            "739482078275",
#                            "Kumar",
#                            "SS Layout, Davangere",
#                            "9382749302",
#                            "kumar@mail.com",
#                            "Architect",
#                            "lic012456",
#                            "02-05-2024"
#     ))
# 
#     cur.execute(commands, ("eng002",
#                            "733484058569",
#                            "Kesar",
#                            "RR Layout, Davangere",
#                            "8562749349",
#                            "kesar@mail.com",
#                            "Structural",
#                            "lic012294",
#                            "02-01-2023"
#     ))
# 
#     cur.close()
#     conn.commit()
# except (Exception, psyco.DatabaseError) as e:
#     print(e)
# finally:
#     if conn is not None:
#         conn.close()
#         print('Database closed')
