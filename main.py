from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import ListProperty
# from kivy.animation import Animation
from kivy.uix.recycleview import RecycleView
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.properties import StringProperty, ColorProperty
from kivymd.uix.dialog import MDDialog
from pokemon import Pokemon
import kivy.utils 
import threading
from kivymd.uix.list import OneLineIconListItem
from kivy.core.text import LabelBase
import requests
from plyer import notification
from kivy.clock import Clock
# from kivymd.uix.menu import MDDropdownMenu
#registering the fonts
LabelBase.register(name='Life', 
                   fn_regular='./new_font/my-life.ttf')
LabelBase.register(name='Lemon', 
                   fn_regular='./new_font/Lemonada-Medium.ttf')
LabelBase.register(name='name_header', 
                   fn_regular='./new_font/Poppins-BoldItalic.ttf')
LabelBase.register(name='type_header', 
                   fn_regular='./new_font/Lemonada-Regular.ttf')
LabelBase.register(name='main-header', 
                   fn_regular='./new_font/Poppins-ExtraBold.ttf')
LabelBase.register(name='numeric', 
                   fn_regular='./new_font/RobotoSlab-SemiBold.ttf')
LabelBase.register(name='text_exp', 
                   fn_regular='./new_font/Lemonada-Medium.ttf')
LabelBase.register(name='tab_header', 
                   fn_regular='./new_font/Poppins-Medium.ttf')
LabelBase.register(name='stat', 
                   fn_regular='./new_font/Raleway-SemiBoldItalic.ttf')
LabelBase.register(name='about', 
                   fn_regular='./new_font/Raleway-MediumItalic.ttf')
Window.size = 400,600
class Intro(MDScreen):
	no_to_load = None
	allowed = False
	text = open('about.txt').read() 
	def clicked(self,value):
		actual_number = None
		if value.isdigit():
			recv_no = int(value)
			if recv_no >=1 and recv_no<=800:
				self.allowed = True
				actual_number = int(recv_no)
			else:
				self.allowed = False
		if self.allowed:
			self.no_to_load = actual_number
		if not(self.allowed):
			self.no_to_load = 850
	def allow_load(self,i,value):
		# print(value)
		if value:
			self.ids.field.opacity = 1
			self.ids.allow_label.opacity = 0
			self.ids.field.readonly = False
			self.ids.add_info.opacity = 1
		else:
			self.ids.field.readonly = True
			self.ids.field.text = ''
			self.ids.add_info.opacity = 0
			self.ids.field.opacity = 0
			self.ids.allow_label.opacity = 1
	def start_dialog(self):
		self.dialog = MDDialog(
			title = 'Getting Information...',
			type="custom",
			content_cls = AppDialog())
		self.dialog.open()
	def eleminate_dialog(self):
		# print(self.dialog)
		self.dialog.dismiss()
class BoxPart(RelativeLayout):
	type_one = StringProperty()
	type_two = StringProperty()
	background_color = ColorProperty()
	name_pokemon = StringProperty()
	pokemon_id = StringProperty()
	pokemon_image = StringProperty()
class PokeViewer(RecycleView):
	no_of_load = None
	color_data = {
	'normal':'#bfbf67', 'fire':'#fd9041',
	'fighting':'#d7261d', 'water':'#5082fb',
	'flying':'#bca6ff', 'grass':'#3ef16d',
	'poison':'#ac1bc1', 'electric':'#ffef32',
	'ground':'#c1951a', 'psychic':'#ff8bae',
	'rock':'#92823a', 'ice':'#a2fafa',
	'bug':'#94a311', 'dragon':'#5c24b8',
	'ghost':'#6e5180', 'dark':'#534338',
	'steel':'#d6d6dd', 'fairy':'#fdcad5',
	}
	all_pokemon_name = {}
	dialog = None
	def __init__(self,**kwags):
		super().__init__(**kwags)
	def no_of_load_set(self,number):
		self.no_of_load = int(number)
		self.start_dialog()
		# print('before ',threading.activeCount())
		th = threading.Thread(target=self.pokemon_data_load)
		th.daemon = True
		th.start()
	def pokemon_data_load(self):
		ending = self.no_of_load + 1
		# print(f'{self.no_of_load} loading' )
		self.data = []
		for i in range(1,int(ending)):		
			poke = Pokemon(i)
			data = poke.pokemon_open_tab()
			# print(data)
			self.set_data_loaded(data)
	def set_data_loaded(self,data):
		pokemon_type_one = None
		pokemon_type_two = None	
		pokemon_id = data[0]
		pokemon_name = data[1]
		self.all_pokemon_name[pokemon_name] = data
		if len(data[2]) == 1:
			pokemon_type_one = data[2][0]
		elif len(data[2]) == 2:
			pokemon_type_one = data[2][0]
			pokemon_type_two = data[2][1]
		pokemon_image = data[3]
		self.add_data_to_block(pokemon_id,pokemon_name,pokemon_type_one,pokemon_type_two,pokemon_image)
		# print(pokemon_id,pokemon_name,pokemon_type_one,pokemon_type_two)
	def add_data_to_block(self,pokemon_id,pokemon_name,pokemon_type_one,pokemon_type_two,pokemon_image):
		self.refresh_from_data()
		self.data.append({
			'viewclass':'BoxPart',
			'type_one':str(pokemon_type_one).title(),
			'type_two':str(pokemon_type_two).title(),
			'background_color':kivy.utils.get_color_from_hex(self.color_data[pokemon_type_one]),
			'name_pokemon':str(pokemon_name.title()),
			'pokemon_id':str(pokemon_id),
			'pokemon_image':str(pokemon_image)})
		if self.no_of_load//2 == 0 or len(self.data) == 5:
			self.eleminate_dialog()
	def add_data(self,text='',allow = True):
		self.data = []
		lp = self.all_pokemon_name.keys()
		for i in lp:
			if allow:
				if text in i :
					# print('\n')
					# print(f'{i} have {text} in it ')
					self.set_data_loaded( self.all_pokemon_name[i])
			else:
				self.set_data_loaded( self.all_pokemon_name[i])
	def start_dialog(self):
		self.dialog = MDDialog(
			title = 'Getting Information...',
			type="custom",
			content_cls = AppDialog())
		self.dialog.open()
	def eleminate_dialog(self):
		# print(self.dialog)
		self.dialog.dismiss()
class PokemonDetails(Screen):
	main_id = None
	def give_data(self,data):
		self.main_id = data
class OpenScreen(MDScreen):
	type_one = StringProperty()
	type_two = StringProperty()
	background_color = ColorProperty()
	pokemon_name = StringProperty()
	pokemon_id = StringProperty()
	pokemon_main_image = StringProperty('image/blank.png')
	main_id = None
	color_data = {
		'normal':'#bfbf67', 'fire':'#fd9041',
		'fighting':'#d7261d', 'water':'#5082fb',
		'flying':'#bca6ff', 'grass':'#3ef16d',
		'poison':'#ac1bc1', 'electric':'#ffef32',
		'ground':'#c1951a', 'psychic':'#ff8bae',
		'rock':'#92823a', 'ice':'#a2fafa',
		'bug':'#94a311', 'dragon':'#5c24b8',
		'ghost':'#6e5180', 'dark':'#534338',
		'steel':'#d6d6dd', 'fairy':'#fdcad5',
		}
	poke = None
	dialog = None
	all_base_data = ListProperty([0,0,0,0,0,0,0])
	def thread_get_mode(self,data):
		# print('before ',threading.activeCount())
		self.main_id = data
		print(self.all_base_data)
		# self.change_remove()
		self.start_dialog()
		th = threading.Thread(target=self.get_data)
		# print('after ',threading.activeCount())
		th.daemon = True
		th.start()
		# th.join()
	def image_background_data(self,dt):
		poke_image = self.poke.pokemon_image()
		self.pokemon_main_image = poke_image
		# print(f'{self.pokemon_main_image}   ======== done')
		self.background_color = kivy.utils.get_color_from_hex(self.color_data[self.poke.pokemon_get_type()[0]])
		# print(self.background_color)
	def get_data(self):
		# self.locked.acquire()
		# print('thread locked')
		self.poke = Pokemon(self.main_id)
		# poke_image = self.poke.pokemon_image()
		# self.pokemon_main_image = poke_image
		# print(f'{self.pokemon_main_image}   ======== done')
		# self.background_color = kivy.utils.get_color_from_hex(self.color_data[self.poke.pokemon_get_type()[0]])
		# print(self.background_color)
		Clock.schedule_once(self.image_background_data,-1)
		pokemon_type_one = None
		pokemon_type_two = None		
		poke_image = self.poke.pokemon_image()
		open_data = self.poke.pokemon_open_tab()
		pokemon_id = open_data[0]
		pokemon_name = open_data[1]
		print(open_data)
		if len(open_data[2]) == 1:
			pokemon_type_one = open_data[2][0]
		elif len(open_data[2]) == 2:
			pokemon_type_one = open_data[2][0]
			pokemon_type_two = open_data[2][1]
		self.background_color = kivy.utils.get_color_from_hex(self.color_data[pokemon_type_one])
		# print(self.background_color)
		self.pokemon_main_image = poke_image
		# print(f'{self.pokemon_main_image}   ======== done')
		self.type_one = str(pokemon_type_one.title())
		self.type_two = str(pokemon_type_two).title()
		self.pokemon_id = str(pokemon_id)
		self.pokemon_name = str(pokemon_name).title()
		self.change_about_page()
		print('about_page_ready')
		Clock.schedule_once(self.tab_value,-1)
		print('tab page ready')
		Clock.schedule_once(self.evolution_tab_data,-1)
		print('evolution page ready')
		move_data = self.poke.pokemon_move_tab()
		for i in move_data:
			self.ids.move_tab.add_move(i)
		self.ids.move_tab.add_move(f'{self.pokemon_name} has {len(move_data)} no. of moves')
		print('move page ready')
		self.eleminate_dialog()

		# self.locked.release()
		# print('thread lock open')
		# print(threading.current_thread())
	def change_about_page(self):
		data = self.poke.pokemon_about_tab()
		self.ids.about_text.text =str(data[0]).replace('\n','').title()
		self.ids.height_value.text = str(data[1])
		self.ids.weight_value.text = str(data[2])
		egg_one = None
		egg_two = None
		if len(data[3]) == 1:
			egg_one = data[3][0]
		elif len(data[3]) == 2:
			egg_one = data[3][0]
			egg_two = data[3][1]
		if str(data[4]) == '-1':
			self.ids.gender_rate.text = '??'
			self.ids.gender_male.text = '??'
		else:
			self.ids.gender_rate.text = str(data[4])+'%'
			self.ids.gender_male.text = str(100-data[4])+'%'
		self.ids.egg_group_one.text = str(egg_one)
		self.ids.egg_group_two.text = str(egg_two)
	def change_remove(self):
		# self.locked.acquire()
		print('main locked')
		self.background_color = kivy.utils.get_color_from_hex('#ffffff')
		self.type_one = ''
		self.type_two = ''
		self.pokemon_id = ''
		self.ids.about_text.text = ''
		self.ids.height_value.text = ''
		self.ids.weight_value.text = ''
		self.pokemon_main_image = 'image/blank.png'
		self.ids.gender_rate.text = str(0)+'%'
		self.ids.egg_group_one.text = ''
		self.ids.egg_group_two.text = ''
		self.all_base_data = [0,0,0,0,0,0,0]
		self.ids.evolve.data = []
		self.ids.move_tab.data = []
		self.ids.evolve.refresh_from_data()
		self.ids.move_tab.refresh_from_data()
		# print(threading.current_thread())
		# print(threading.activeCount())
		# self.locked.release()
		print('main open')
	def evolution_tab_data(self,dt):
		print(dt)
		evolution,image = self.poke.pokemon_evolution_tab()
		evolution = list(evolution)
		if len(evolution)==0 or not len(evolution[0][1]):
			self.ids.evolve.set_data(None,None,self.pokemon_name,None,self.pokemon_main_image,None,None,True)
		elif len(evolution) == 1 and len(evolution[0][1]):
			base_stage = evolution[0][0]
			# print(base_stage)
			for j in range(len(evolution[0][1])):
				if j%2 == 0:
					final_stage = evolution[0][1][j]
					base_image = image[base_stage]
					final_image = image[final_stage]
					# print(final_image,final_stage)
					extra = evolution[0][1][j+1].item 
					min_lev = evolution[0][1][j+1].min_level
					type_elv = evolution[0][1][j+1].trigger.name
					self.ids.evolve.set_data(extra,min_lev,base_stage,final_stage,base_image,final_image,type_elv)
		elif len(evolution) == 2 and len(evolution[0][1]):
			for i in evolution:
				base_stage = i[0]
				# print(base_stage)
				for j in range(len(i[1])):
					if j%2 == 0:
						final_stage = i[1][j]
						base_image = image[base_stage]
						final_image = image[final_stage]
						# print(final_image,final_stage)
						extra = i[1][j+1].item 
						min_lev = i[1][j+1].min_level
						type_elv = i[1][j+1].trigger.name
				self.ids.evolve.set_data(extra,min_lev,base_stage,final_stage,base_image,final_image,type_elv)
	def start_dialog(self):
		self.dialog = MDDialog(
			title = 'Getting Information...',
			type="custom",
			content_cls = AppDialog())
		self.dialog.open()
	def eleminate_dialog(self):
		self.dialog.dismiss()
		self.dialog = None
	def tab_value(self,dt):
		print(dt)
		self.all_base_data = self.poke.pokemon_stat_tab()
class Evolution(RelativeLayout):
	item = StringProperty()
	level = StringProperty()
	elv_type = StringProperty()
	name_back = StringProperty()
	name_front = StringProperty()
	poke_back = StringProperty()
	poke_front = StringProperty()
class EvolvePart(RecycleView):
	def __init__(self,**kwags):
		super().__init__(**kwags)
		self.data = []
	def set_data(self,item,level,name_back,name_front,
		poke_back,poke_front,trigger,diffrent = False):
		if not diffrent:
			self.refresh_from_data()
			item_needed = 'None'
			if trigger == 'use-item':
				try:
					item_needed = str(item.name)
				except:
					item_needed  = ''
			self.data.append({
				'viewclass':'Evolution',
				'item':str(item_needed).title(),
				'level':str(level).title(),
				'name_back':str(name_back).title(),
				"name_front":str(name_front).title(),
				'poke_back':str(poke_back),
				'poke_front':str(poke_front),
				'elv_type':str(trigger).title() 
				})
			# print(self.data,'\n',len(self.data))
		else:
			self.refresh_from_data()
			self.data.append({
				'viewclass':'Evolution',
				'item':'Evolution',
				'level':'has no',
				'name_back':' ',
				'poke_back':str(poke_back),
				'name_front':' ',
				'poke_front':str(poke_back),
				'elv_type':str(name_back) 
				})
			# print(self.data,'\n',len(self.data))
class MoveTab(RecycleView):
	def __init__(self,**kwags):
		super().__init__(**kwags)
		self.data = []
	def add_move(self,move_name):
		self.refresh_from_data()
		self.data.append({
			'viewclass':'MoveTabContent',
			'move_name':str(move_name)
				})
class MoveTabContent(OneLineIconListItem):
	move_name = StringProperty()


class AppDialog(Screen):
	text = 'Please Wait its loading\n'


class SomeText(MDScreen):
	text = open('about.txt').read()


class PokeDex(MDApp):
	def build(self):
		if self.get_internet_connection():
			kv_file = Builder.load_file('main.kv')
		else:
			kv_file = Builder.load_file('secondary.kv')
		return kv_file
	def get_internet_connection(self):
		allowed = False
		try:
			run = requests.get('http://www.google.com',timeout=2)
			allowed = True
		except requests.exceptions.ConnectionError as e:
			print(e)
		if allowed:
			message_text = 'Internet Connection Available'
		else:
			message_text = 'App Requires A Internet Connection'
		notification.notify(
			title = 'PokeDex',
			message = message_text,
			app_icon='image/notify_icon.ico',
			timeout = 1,
			)
		return allowed
if __name__ =='__main__':
	PokeDex().run()