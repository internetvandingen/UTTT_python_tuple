import pickle
import json
import yapf

from pprint import pprint
# pip install yapf

if __name__ == '__main__':
	
	# opens pickle 'file' and converts all tuple keys to string keys so the dictionary can be dumped with json in 'temp.json'
	file = '_Q1000.p'
	


	with open(file, 'rb') as handle:
		d = pickle.load(handle)



	nr_games = d.pop('nr_games', None)
	newd = {''.join(map(str, key)):{''.join(map(str, subkey)): d[key][subkey] for subkey in d[key]} for key in d}
	newd['nr_games'] = nr_games


	# style = { 'COLUMN_LIMIT': 100, 'ALLOW_SPLIT_BEFORE_DICT_VALUE': False}
	# text, flag = yapf.yapflib.yapf_api.FormatCode(str(newd), style_config=style)
	# print(text)

	# save file in readable json format, open with sublime text and reformat with Ctrl+Alt+f if JsFormat-master package is installed
	with open('temp.json', 'w') as handle:
		json.dump(newd, handle)
