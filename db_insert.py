import db
import psycopg2 as psyco

conn = None
try:
    conn = db.connect_db()
    cur = conn.cursor()

    commands = (
        """
        INSERT INTO GramPanchayat (
            gram_id, 
            gram_name,
            g_district,
            g_state
        )
        VALUES (
            %s,
            %s,
            %s,
            %s
        )
        """
    )

    cur.execute(commands, ('gram001', 'ketu gram', 'Davangere', 'Karnataka'))
    cur.execute(commands, ('gram002', 'Harihar', 'Davangere', 'Karnataka'))

    cur.close()
    conn.commit()
except (Exception, psyco.DatabaseError) as e:
    print(e)
finally:
    if conn is not None:
        conn.close()
        print('Database closed')
