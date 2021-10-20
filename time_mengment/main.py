from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup , ReplyKeyboardMarkup , KeyboardButton
from telegram.ext import Updater , CommandHandler , MessageHandler , Filters , CallbackQueryHandler
import datetime
import time
from for_data import *
from ast import literal_eval
def ktb(type,ctg=None,son=None):
	if type=="main":
		btn=[[InlineKeyboardButton("🏃🏃‍♀️ Foydali mashg'ulot",callback_data='foydali'),InlineKeyboardButton("📊 Reja qo'shish",callback_data='reja+')],
		[InlineKeyboardButton("⚒ Bajarilayotgan reja" , callback_data='breja'),InlineKeyboardButton("🔚 Rejani bekor qilish",callback_data='reja-')],
		[InlineKeyboardButton('📖 Bot haqida' , callback_data='bot haqida')]]
	elif type=='reja':
		btn=[[InlineKeyboardButton('🕝 Soatlik', callback_data=f"{ctg}_1"),InlineKeyboardButton('📅 Kunlik', callback_data=f"{ctg}_2")],
		[InlineKeyboardButton('📆 Haftalik', callback_data=f"{ctg}_3")],
		[InlineKeyboardButton('🔙 Orqaga', callback_data=f"{ctg}_orqaga")]]	
	return InlineKeyboardMarkup(btn)







def start(update, context):
	user=update.message.from_user
	insert_log(user.id)
	update.message.reply_html("<b>Assalomu alaykum bu bot orqali siz o'z rejalaringiz o'z vaqtida bajarishingizni yordam beradi</b>.")
	time.sleep(1)
	update.message.reply_text("Quydagilardan birini tanlang ✅" , reply_markup=ktb('main') )
def message_for(update,context):
	msg=update.message.text
	user=update.message.from_user
	qadam=get_log(user.id)
	qadam=qadam[0].split('_')
	

	if qadam[0]=='1' :
		reja_id=qadam[1]
		update_log(user.id ,'0')
		times=(datetime.datetime.now()).strftime("%c")
		ids=none(user.id,int(reja_id))[-1][0]
		update_plan(int(reja_id),user.id, msg , f'{times}' , ids)
		update.message.reply_text("Rejangiz qo'shildi",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]))
		

	elif qadam[0]=='3':
		user=update.message.from_user
		times=(datetime.datetime.now()).strftime("%c")
		insert_foy(msg,times,user.id)
		update.message.reply_text("Foydali mashg'ulot qo'shildi ➕",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]))
			
def callback(update , context):
	user=update.callback_query.from_user
	print(user.id)
	data=update.callback_query.data
	print(data)
	data_sp=data.split('_')
	if data_sp[0]=='foydali':
		btn=InlineKeyboardMarkup([[InlineKeyboardButton("➕ Qo'shish", callback_data="qo'shish"),InlineKeyboardButton("🔎 Ko'rish", callback_data="ko'rish")],
			[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]])
		update.callback_query.message.edit_text('Nima qilmoqchisiz', reply_markup=btn)
	elif data_sp[0]=="qo'shish" :
		update_log(user.id , f"3")
		context.bot.delete_message(message_id=update.callback_query.message.message_id,chat_id=update.callback_query.message.chat_id)
		context.bot.send_message(text="Foydali mashug'lot matnini kiriting 🔎",chat_id=update.callback_query.message.chat_id)

	elif data_sp[0]=="ko'rish":
		text=select_foy(user.id)
		if text:
			s=''
			j=0
			for i in text:
				j+=1
				s+=f'{j}) '+i[0]+'\n'
			update.callback_query.message.edit_text(f"Sizda quydagi foydali mashg'ulot \n {s} ",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]) )
		else :
			update.callback_query.message.edit_text("Sizda hali foydali mashg'ulot qo'shilmagan 🤷‍♂🤷‍♂🤷‍♂🤷‍♂",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]))

	elif data_sp[0]=='bot haqida'and len(data_sp)==1:
		update_log(user.id , "2")
		update.callback_query.message.edit_text("Ushbu bot orqali siz o'zngiz uchun muhim ishlarni eslatib turuvchi dastur sifatida foydalanishingiz mumkin. ",
		reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]))
	elif len(data_sp)>1 :
		if data_sp[0]=='reja+' and data_sp[1]!='orqaga':
			insert_plan(user.id,int(data_sp[1]))
			update_log(user.id , f"1_{data_sp[1]}")
			context.bot.delete_message(message_id=update.callback_query.message.message_id,chat_id=update.callback_query.message.chat_id)
			context.bot.send_message(text='Reja matnini kiriting ',chat_id=update.callback_query.message.chat_id)
		elif data_sp[1]=='orqaga':
			update.callback_query.message.edit_text("Quydagilardan birini tanlang ✅" , reply_markup=ktb('main') )
		elif data_sp[0]=='breja':
			text=select_plan(user.id,int(data_sp[1]))
			if text :
				if data_sp[1]=='1' and text!=None and data_sp[0]=='breja':
					s=''
					j=0
					for i in text:
						j+=1
						natija=i[1].split(' ')
						n=natija[4].split(':')
						soat=int(n[0])+1
						n[0]=str(soat)
						d=n[0]+':'+n[1]+':'+n[2]
						s+=f'{j}) '+i[0]+'\n '+'boshlangan vaqti'+' '+f'{i[1]}'+'\n'+'tugash vaqti'+' '+f'{d}'+'\n'
					context.bot.send_message(text=f'Bajarilmoqda ⚒\n {s}' , chat_id=update.callback_query.message.chat_id,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]))
					
				elif data_sp[1]=='2' and text!=None and data_sp[0]=='breja':
					s=''
					j=0
					for i in text:
						j+=1
						natija=i[1].split(' ')
						natija[3]=int(natija[3])+1
						d=natija[0]+' '+natija[1]+' '+natija[2]+' '+str(natija[3])+' ' +natija[4]+''+natija[5]
						s+=f'{j}) '+i[0]+'\n '+'boshlangan vaqti'+' '+f'{i[1]}'+'\n'+'tugash vaqti'+' '+f'{d}'+'\n'
					
					context.bot.send_message(text=f'Bajarilmoqda ⚒\n {s}' , chat_id=update.callback_query.message.chat_id,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]))
					
				elif data_sp[1]=='3' and text!=None and data_sp[0]=='breja':
					s=''
					j=0
					for i in text:
						j+=1
						natija=i[1].split(' ')
						natija[3]=int(natija[3])+7
						d=natija[0]+' '+natija[1]+' '+natija[2]+' '+str(natija[3])+' ' +natija[4]+''+natija[5]
						s+=f'{j}) '+i[0]+'\n '+'boshlangan vaqti'+' '+f'{i[1]}'+'\n'+'tugash vaqti'+' '+f'{d}'+'\n'
					
					context.bot.send_message(text=f'Bajarilmoqda ⚒\n {s}' , chat_id=update.callback_query.message.chat_id,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]))
			else :
				update.callback_query.message.edit_text("Sizda bu turdagi reja yo'q 🤷‍♂🤷‍♂🤷‍♂🤷‍♂",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]))


		elif data_sp[0]=="reja-" and len(data_sp)!=3:
			text=select_plan(user.id,int(data_sp[1]))
			if text :
				if data_sp[1]=='1' and text!=None and data_sp[0]=='reja-':
					s=''
					j=0
					btn=[]
					for i in text:
						j+=1
						natija=i[1].split(' ')
						n=natija[4].split(':')
						soat=int(n[0])+1
						n[0]=str(soat)
						d=n[0]+':'+n[1]+':'+n[2]
						s+=f'{j}) '+i[0]+'\n '+'boshlangan vaqti'+' '+f'{i[1]}'+'\n'+'tugash vaqti'+' '+f'{d}'+'\n'
					
					for j in range(0,len(text)-1,2):
						a=[InlineKeyboardButton(f'{j+1}',callback_data=f'reja-_1_{text[j][1]}'),
						InlineKeyboardButton(f'{j+2}',callback_data=f'reja-_1_{text[j+1][1]}')]
						btn.append(a)
					if len(text)%2==1:
						a=[InlineKeyboardButton(f'{len(text)}', callback_data=f'reja-_1_{text[-1][1]}')]
						btn.append(a)
					update.callback_query.message.edit_text(f"Bekor qilmoqchi bo'lgan rejani  tanlang ✅\n {s}", reply_markup=InlineKeyboardMarkup(btn))
				elif data_sp[1]=='2'and text!=None and data_sp[0]=='reja-':
					s=''
					j=0
					btn=[]
					for i in text:
						j+=1
						natija=i[1].split(' ')
						natija[3]=int(natija[3])+1
						d=natija[0]+' '+natija[1]+' '+natija[2]+' '+str(natija[3])+' ' +natija[4]+''+natija[5]
						s+=f'{j}) '+i[0]+'\n '+'boshlangan vaqti'+' '+f'{i[1]}'+'\n'+'tugash vaqti'+' '+f'{d}'+'\n'

					for j in range(0,len(text)-1,2):
						a=[InlineKeyboardButton(f'{j+1}',callback_data=f'reja-_1_{text[j][1]}'),
						InlineKeyboardButton(f'{j+2}',callback_data=f'reja-_1_{text[j+1][1]}')]
						btn.append(a)
					if len(text)%2==1:
						a=[InlineKeyboardButton(f'{len(text)}', callback_data=f'reja-_1_{text[-1][1]}')]
						btn.append(a)
					update.callback_query.message.edit_text(f"Bekor qilmoqchi bo'lgan rejani  tanlang ✅\n {s}", reply_markup=InlineKeyboardMarkup(btn))
				elif data_sp[1]=='3'and text!=None and data_sp[0]=='reja-':
					s=''
					j=0
					btn=[]
					for i in text:
						j+=1
						natija=i[1].split(' ')
						natija[3]=int(natija[3])+7
						d=natija[0]+' '+natija[1]+' '+natija[2]+' '+str(natija[3])+' ' +natija[4]+''+natija[5]
						s+=f'{j}) '+i[0]+'\n '+'boshlangan vaqti'+' '+f'{i[1]}'+'\n'+'tugash vaqti'+' '+f'{d}'+'\n'
					for j in range(0,len(text)-1,2):
						a=[InlineKeyboardButton(f'{j+1}',callback_data=f'reja-_1_{text[j][1]}'),
						InlineKeyboardButton(f'{j+2}',callback_data=f'reja-_1_{text[j+1][1]}')]
						btn.append(a)
					if len(text)%2==1:
						a=[InlineKeyboardButton(f'{len(text)}', callback_data=f'reja-_1_{text[-1][1]}')]
						btn.append(a)
					update.callback_query.message.edit_text(f"Bekor qilmoqchi bo'lgan rejani  tanlang ✅\n {s}", reply_markup=InlineKeyboardMarkup(btn))	
			else :
				update.callback_query.message.edit_text("Sizda bu turdagi reja yo'q 🤷‍♂🤷‍♂🤷‍♂🤷‍♂",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]))


		elif len(data_sp)==3:
			del_plan(data_sp[2])
			context.bot.send_message(text='Reja bekor qilindi' , chat_id=update.callback_query.message.chat_id,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Orqaga', callback_data="reja+_orqaga")]]))
		
 			


	else:
		update.callback_query.message.edit_text("📅 Reja muddatini tanlang ✅", reply_markup=ktb('reja',ctg=data_sp[0]))	






def main():
	TOKEN="1969862768:AAHUa2dZDbmcxKy7b5kLsYBrr2YIJJ30J68"
	updater=Updater(TOKEN)
	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(MessageHandler(Filters.text , message_for))
	updater.dispatcher.add_handler(CallbackQueryHandler(callback))
	updater.start_polling()
	updater.idle()	

if __name__=="__main__":
	main()
















