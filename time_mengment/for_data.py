import sqlite3 
conn=sqlite3.connect('time.db',check_same_thread=False)
cur=conn.cursor()

#1 bu funksiyalar reja qoshish uchun
def insert_plan(user_id,plan_id):
	sql=f"""
		insert into plan(user_id ,reja_id )values({user_id},{plan_id})
	"""
	cur.execute(sql)
	conn.commit()
	sql1=f"""
		sel
	"""





def update_plan(reja_id , user_id , msg , time, id):
	sql=f"""
	update plan set rejatext="{msg}" , time="{time}" where reja_id={reja_id} and user_id={user_id} and id={id}
	"""
	cur.execute(sql)
	conn.commit()
def select_plan(user_id,plan_id):
	sql= f""" 
	select rejatext , time from plan where user_id={user_id} and reja_id={plan_id}
	"""
	cur.execute(sql)
	return cur.fetchall()
def del_plan(time):
	sql=f"""delete from plan where time="{time}" """
	cur.execute(sql)
	conn.commit()





def none(user_id,plan_id):
	sql=f""" select id from plan 
	 """
	cur.execute(sql)
	return cur.fetchall()
print(none(1157247305,1)[-1][0])

# bu funksiyalar qadam olish uchun

def insert_log(user_id):
	try :
		sql= f""" 
			insert into user_log(user_id , qadam )values({user_id},0)
		"""	
		cur.execute(sql)
		conn.commit()
	except :
		pass	
#insert_log(1402555366666)	
def update_log(user_id, log):
	sql=f"""
		update user_log set qadam="{log}" where user_id={user_id}
	"""
	cur.execute(sql)
	conn.commit()
	return get_log(user_id)

#update_log(1402555366666,1)
def get_log(user_id):
	sql=f"""
		select qadam from user_log where user_id={user_id}
	"""
	cur.execute(sql)
	return cur.fetchone()
#print((get_log(1402555366666))[0])
def insert_foy(text, time,user_id):
	sql=f"""
	insert into foydali(foydalitext,foydalitime,user_id)values("{text}","{time}","{user_id}")
	"""
	cur.execute(sql)
	conn.commit()
def select_foy(user_id):
	sql=f""" 
	select foydalitext,foydalitime from foydali where user_id="{user_id}"
	"""
	cur.execute(sql)
	return cur.fetchall()
print(select_foy(1157247305))