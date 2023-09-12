import psycopg2
con1 = psycopg2.connect(
    host = "localhost",
    database = "bookProject",
    user = "postgres",
    password="12345678"
)
con2 = psycopg2.connect(
    host = "localhost",
    database = "second_db",
    user = "postgres",
    password="12345678"
)
con2.autocommit =True
con1.autocommit =True
cur = con1.cursor()
cur_2 = con2.cursor()

# get names of tables from first db
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema='public';")
temp = cur.fetchall()
table_name = []
for r in temp:
    table_name.append(r[0])
# get attribute for each table
attr = {}
for x in table_name:
    attr[x] = []
    cmd = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = '{}';"
    cur.execute( cmd.format(x))
    temp = cur.fetchall()
    for r in temp:
        attr[x].append(r[0])

# get foreign key list for tables
fk_list = {}
for x in table_name:
    fk_list [x]= []
    cmd = "SELECT distinct ccu.table_name AS foreign_table_name FROM information_schema.table_constraints AS tc  JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema  JOIN information_schema.constraint_column_usage AS ccu   ON ccu.constraint_name = tc.constraint_name  AND ccu.table_schema = tc.table_schema WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='{}';"
    cur.execute(cmd.format(x))
    temp = cur.fetchall()
    for r in temp:
        fk_list[x].append(r[0])
# get primary key list for tables
pk_list = {}
for x in table_name:
    pk_list[x]=[]
    cmd = "SELECT    pg_attribute.attname FROM pg_index, pg_class, pg_attribute, pg_namespace  WHERE  pg_class.oid = '{}'::regclass AND   indrelid = pg_class.oid AND   nspname = 'public' AND   pg_class.relnamespace = pg_namespace.oid AND  pg_attribute.attrelid = pg_class.oid AND   pg_attribute.attnum = any(pg_index.indkey) AND indisprimary;"
    cur.execute(cmd.format(x))
    temp = cur.fetchall()
    for r in temp:
        pk_list[x].append(r[0])
# sort table name by dag
temp = []
while len(table_name)>0:
    root =""
    for x in table_name:
        if(len(fk_list[x]) == 0):
            root = x
            break
    temp.append(root)
    table_name.remove(root)
    for x in table_name:
        if( fk_list[x].count(root )> 0):
            fk_list[x].remove(root)
table_name = temp

# pk num in attribute list
pk_num = {}
for x in table_name:
    j = 0
    pk_num[x] = []
    for i in range(len(pk_list[x])) :
        while pk_list[x][i] != attr[x][j] :
            j+=1
        pk_num[x].append(j)
for name in table_name:
    cmd = "select count (*) from {};"
    cur.execute(cmd.format(name))
    cnt = cur.fetchall()[0][0]
    for x in range(cnt) :
        cmd = "select * from {} offset {} limit 1 ;"
        cur.execute(cmd.format(name, x))
        row = cur.fetchall()
        row = row[0]
        cmd = "select * from {} where "
        for i in range(len(pk_list[name])):
            cmd += pk_list[name][i] + " = '" + str(row[pk_num[name][i]]) + "',"
        cmd = cmd[:len(cmd) - 1]
        cmd += ";"
        cur_2.execute(cmd.format(name))
        temp = cur_2.fetchall()
        # insert
        if (len(temp) ==0):
            cmd = "INSERT INTO {} VALUES ("
            for z in row :
                    cmd += "'"+str(z) +"',"
            cmd = cmd[:len(cmd)-1]
            cmd +=");"
            cur_2.execute(cmd.format(name))
        # update
        else:
            cmd = ""
            for z in range(len(row)):
                if temp[0][z] != row[z]:
                    cmd += attr[name][z] + " = '"+str (row[z])+"' ,"
            if len(cmd) > 0:
                cmd = "update {} set "+cmd
                cmd = cmd[:len(cmd)-1]
                cmd += "where "
                for i in range(len(pk_list[name])):
                    cmd += pk_list[name][i] + " = '" + str(row[pk_num[name][i]]) + "',"
                cmd = cmd[:len(cmd) - 1]
                cmd += ";"
                cur_2.execute(cmd.format(name))
    # delete
    cmd = "select count(*) from {};"
    cur_2.execute(cmd.format(name))
    cnt = cur_2.fetchall()[0][0]
    for x in range(cnt):
        cmd = "select * from {} offset {} limit 1 ;"
        cur_2.execute(cmd.format(name,x))
        row = cur_2.fetchall()
        row = row[0]
        cmd = "select * from {} where "
        cmd_1=""
        for i in range(len(pk_list[name])):
            cmd_1 += pk_list[name][i] + " = '" + str(row[pk_num[name][i]]) + "',"
        cmd_1= cmd_1[:len(cmd_1) - 1]
        cmd_1 += ";"
        cmd += cmd_1
        cur.execute(cmd.format(name))
        temp = cur.fetchall()
        if len(temp) == 0:
            cmd = "delete from {} where " + cmd_1
            cur_2.execute(cmd.format(name))