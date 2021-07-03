
import pokepy
from beckett.exceptions import InvalidStatusCodeError
class Pokemon:
	def __init__(self,name):
		self.name = name
		self.clt = pokepy.V2Client(cache='in_disk', cache_location='.')
		self.pokemon_obj = None
		self.pokemon_details = None
		self.pokemon_valid()
		self.name = self.pokemon_obj.name
		self.height = self.pokemon_obj.height
		self.weight = self.pokemon_obj.weight
		self.id = self.pokemon_obj.id
	def pokemon_valid(self):
		try:
			self.pokemon_obj = self.clt.get_pokemon(self.name)
		except InvalidStatusCodeError:
			print('Pokemon dont exists')
		except ConnectionError:
			print('No Internet Found')
	def pokemon_get_type(self):
		poke_type = list()
		if self.pokemon_obj:
			for i in self.pokemon_obj.types:
				poke_type.append(i.type.name)
		else:
			print('a corrent obj is required')
		return poke_type
	def pokemon_get_ability(self):
		poke_ability = list()
		if self.pokemon_obj:
			for i in self.pokemon_obj.abilities:
				poke_ability.append(i.ability.name)
		else:
			print('a correct obj')
		return poke_ability
	def pokemon_image(self):
		poke_id = self.pokemon_obj.id
		if len(str(poke_id)) == 1:
			poke_id = '00' + str(int(poke_id))
		elif len(str(poke_id)) == 2:
			poke_id = '0' + str(int(poke_id))
		elif len(str(poke_id)) == 2:
			poke_id = str(int(poke_id))
		url = f'https://assets.pokemon.com/assets/cms2/img/pokedex/full/{poke_id}.png'
		return url
	def pokemon_evolution(self,name):
		self.pokemon_details = self.clt.get_pokemon_species(name)
		if self.pokemon_details:
			data_set = dict()
			ev_url = self.pokemon_details.evolution_chain.url
			ev_id = str(ev_url).replace('https://pokeapi.co/api/v2/evolution-chain/','')
			ev_object = self.clt.get_evolution_chain(ev_id).chain
			if 'evolves_to'in dir(ev_object) and len(ev_object.evolves_to)  :
				data_set[name] =  list()
				# print(ev_object,ev_object.evolves_to)
				for i in ev_object.evolves_to:
					if  len(i.evolution_details):
						# print('True')
						data_set[name].extend([i.species.name,i.evolution_details[0]])
					if 'evolves_to' in dir(i) and len(i.evolves_to) :
						data_set[i.species.name] =  list()
						for j in i.evolves_to:
							if  len(j.evolution_details):
								data_set[i.species.name].extend([j.species.name,
								j.evolution_details[0]])
		return data_set
	def pokemon_get_baby(self,name):
		poke_name = None
		self.pokemon_details = self.clt.get_pokemon_species(name)
		if self.pokemon_details:
			if  self.pokemon_details.evolves_from_species :
				name = self.pokemon_details.evolves_from_species.name
				if  self.clt.get_pokemon_species(name).evolves_from_species:
					name = self.clt.get_pokemon_species(name).evolves_from_species.name
					poke_name = name
				else:
					poke_name = name
			else:
				poke_name = name
		return poke_name
	def pokemon_get_images(self,name):
		poke_image = None
		if name:
			poke_image = self.clt.get_pokemon(name).sprites.front_default
		# print(poke_image)
		return poke_image
	def pokemon_evolution_tab(self):
		name = self.pokemon_obj.name
		baby_pokemon = self.pokemon_get_baby(name)
		evolution = self.pokemon_evolution(baby_pokemon).items()
		# print(evolution)
		image = dict()
		for i in list(evolution):
			image[i[0]] = self.pokemon_get_images(i[0])
			for j in i[1]:
				if (i[1].index(j)%2) == 0:
					image[j] = self.pokemon_get_images(j)
		return evolution,image
	def pokemon_stat_tab(self):
		poke_value = list()
		total = 0
		if self.pokemon_obj:
			for i in self.pokemon_obj.stats:
				poke_value.append(int(i.base_stat))
				total+=int(i.base_stat)
			poke_value.append(total)
		else:
			print('A correct object is required')
		return poke_value
	def pokemon_about_tab(self):
		poke_obj =  self.clt.get_pokemon_species(self.name)
		text = poke_obj.flavor_text_entries[0].flavor_text
		for i in poke_obj.flavor_text_entries:
			if i.language.name == 'en':
				text = i.flavor_text
		height = self.height
		weight = self.weight
		if poke_obj.gender_rate != -1:
			gender = (int(poke_obj.gender_rate)/8)*100
		else:
			gender = int(poke_obj.gender_rate)
		egg = list()
		for i in poke_obj.egg_groups:
			egg.append(i.name)
		value = [text,height,weight,egg,gender]
		return value
	def pokemon_move_tab(self):
		poke_obj = self.pokemon_obj
		move_list = list()
		for i in poke_obj.moves:
			move_list.append((i.move.name).title())
		return move_list
	def pokemon_open_tab(self):
		poke_id = self.id 
		poke_name = self.name 
		poke_image = self.pokemon_get_images(poke_name)
		poke_type = self.pokemon_get_type()
		return poke_id,poke_name,poke_type,poke_image
