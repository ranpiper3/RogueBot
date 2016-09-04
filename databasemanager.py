import config
from tinydb import TinyDB, Query

VAR_TABLE = 'vars'
ROOMS_TABLE = 'rooms'
KILLS_TABLE = 'kills'
GNOME_TABLE = 'gnome'
RATE_TABLE = 'rate'

db = TinyDB(config.DATABASE_PATH)

def get_variable(name, def_val=None):
	global db
	Variable = Query()

	table = db.table(VAR_TABLE)
	ans = table.get(Variable.name == name)
	if ans:
		return ans['value']
	else:
		return def_val

def set_variable(name, value):
	global db

	table = db.table(VAR_TABLE)
	return table.insert({'name':name,'value':value})

def add_to_leaderboard(user, score, reason=None, leaderboard_name='rate'):
	global db

	table = db.table(leaderboard_name)
	doc = {
		'uid': user.uid,
		'name': user.name,
		'score': score,
		'reason': reason
	}
	table.insert(doc)

def get_leaderboard(leaderboard_name='rate', count=10):
	global db

	if leaderboard_name not in db.tables():
		return [ ]

	def sort_by_score(doc):
		return doc['score']

	table = db.table(leaderboard_name)

	res = table.all()
	res.sort(key=sort_by_score, reverse=True)

	return res[:count]