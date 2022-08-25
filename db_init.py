import db
import psycopg2 as psyco

def exec_once():
    """Exec Once"""
    conn = None
    try:
        conn = db.connect_db()
        cur = conn.cursor()

        commands = ("""
            CREATE TABLE IF NOT EXISTS Engineering (
                eng_id      VARCHAR(10) PRIMARY KEY,
                eng_aadhar  VARCHAR(12),
                eng_name    VARCHAR(30),
                eng_address VARCHAR(100),
                eng_mobile  VARCHAR(10),
                eng_email   VARCHAR(30),
                eng_role    VARCHAR(20),
                license_no  VARCHAR(30),
                valid_upto  VARCHAR(10)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Client (
                cli_id      VARCHAR(10) PRIMARY KEY,
                cli_aadhar  VARCHAR(12),
                cli_name    VARCHAR(30),
                cli_address VARCHAR(100),
                cli_mobile  VARCHAR(10),
                cli_email   VARCHAR(30)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Project (
                project_id  VARCHAR(10),
                cli_id      VARCHAR(10),
                eng_id      VARCHAR(10),
                gram_id     VARCHAR(10)
            )
            """,
            """
            ALTER TABLE Project
            ADD CONSTRAINT clie_id
            FOREIGN KEY(cli_id) REFERENCES Client(cli_id)
            ON DELETE CASCADE
            """,
            """
            ALTER TABLE Project
            ADD CONSTRAINT enge_id
            FOREIGN KEY(eng_id) REFERENCES Engineering(eng_id)
            ON DELETE CASCADE
            """,
            """CREATE TABLE IF NOT EXISTS GramPanchayat (
                gram_id     VARCHAR(10) PRIMARY KEY,
                gram_name   VARCHAR(30),
                g_district  VARCHAR(30),
                g_state     VARCHAR(30),
                j_rules     JSONB,
                j_docs      JSONB
            )
            """,
            """
            ALTER TABLE Project
            ADD CONSTRAINT grae_id
            FOREIGN KEY(gram_id) REFERENCES GramPanchayat(gram_id)
            ON DELETE CASCADE
            """,
            """
            ALTER TABLE Project
            ADD CONSTRAINT pro_prim
            PRIMARY KEY(project_id)
            """,
            """
            CREATE TABLE IF NOT EXISTS GramEmployee (
                emp_aadhar  VARCHAR(12),
                emp_name    VARCHAR(30),
                emp_address VARCHAR(100),
                emp_mobile  VARCHAR(10),
                emp_id  VARCHAR(10) PRIMARY KEY,
                emp_email   VARCHAR(30),
                emp_role    VARCHAR(20),
                work_count  INT,
                gram_id     VARCHAR(10),
                points      INT,
                account_status CHAR,
                missed_deadlines INT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS FailedTasks (
                project_id  VARCHAR(10),
                emp_id      VARCHAR(10),
                reason      VARCHAR(300)
            )
            """,
            """
            ALTER TABLE FailedTasks
            ADD CONSTRAINT pr_id_f
            FOREIGN KEY(project_id) REFERENCES Project(project_id)
            ON DELETE CASCADE
            """,
            """
            ALTER TABLE FailedTasks
            ADD CONSTRAINT em_id_f
            FOREIGN KEY(emp_id) REFERENCES GramEmployee(emp_id)
            ON DELETE CASCADE
            """,
            """
            CREATE TABLE IF NOT EXISTS ProjectStatus (
                project_id  VARCHAR(10),
                emp_id      VARCHAR(10),
                assign_date VARCHAR(10),
                p_step      VARCHAR(20)
            )
            """,
            """
            ALTER TABLE ProjectStatus
            ADD CONSTRAINT prid_f
            FOREIGN KEY(project_id) REFERENCES Project(project_id)
            ON DELETE CASCADE
            """,
            """
            ALTER TABLE ProjectStatus
            ADD CONSTRAINT emid_f
            FOREIGN KEY(emp_id) REFERENCES GramEmployee(emp_id)
            ON DELETE CASCADE
            """,
            """
            CREATE TABLE IF NOT EXISTS Rules (
                ruleSection VARCHAR(30),
                subrule     VARCHAR(600)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ShareProject (
                from_emp    VARCHAR(10),
                to_emp      VARCHAR(10),
                missed      CHAR
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Payment (
                project_id  VARCHAR(10),
                pay_date    VARCHAR(10),
                tran_id     VARCHAR(24),
                paid_to     VARCHAR(20),
                paid_from   VARCHAR(20)
            )
            """
        )

        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
    except (Exception, psyco.DatabaseError) as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
            print('Database closed')

one = exec_once()
