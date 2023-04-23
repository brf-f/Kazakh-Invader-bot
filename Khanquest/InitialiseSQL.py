import sqlite3

def init(db, crtTbl, initTblVals, InsrtCmd):
    #connect to database
    c = sqlite3.connect(db)
    cursor = c.cursor()

    try:
        cursor.execute(crtTbl)

        newTblVals = initTblVals
        cursor.executemany(InsrtCmd,newTblVals)
        c.commit()
        print("Table created")
        
    except sqlite3.OperationalError:
        print("Table Exists")
        pass

    c.close()