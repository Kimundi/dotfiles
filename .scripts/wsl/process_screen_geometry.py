#!/usr/bin/env python3

import sys
import re
import pprint

def load_str(path):
	r = ""
	with open(path, 'r') as f:
		r = f.read()
	return r
def write_str(path, data):
	with open(path, 'w') as f:
		f.write(data)

geometry_file = sys.argv[1]
i3config_file = sys.argv[2]
geometry_raw = load_str(geometry_file).strip()

geometry = re.findall("DeviceName.*?:(.*?)Primary.*?:(.*?)WorkingArea.*?:.*?\{(.*?)\}", geometry_raw, re.S)

geometries = []
for (name, primary, geo) in geometry:
	name = name.strip()
	if name.startswith("\\\\.\\"):
		name = name[4:]
	primary = primary.strip() == "True"
	geo = dict(map(lambda vs: vs.split("="), geo.split(",")))
	for k in geo:
		geo[k] = int(geo[k])
	geometries.append((name, primary, geo))
geometries.sort(key=lambda x: not x[1])
if len(geometries) == 0:
    sys.exit(0)

x = 0
y = 0
w = 0
h = 0

for (name, primary, geo) in geometries:
	x = min(x, geo["X"])
	y = min(y, geo["Y"])
	w = max(w, geo["X"] + geo["Width"])
	h = max(h, geo["Y"] + geo["Height"])

offx = -x
offy = -y

i3_strs = []
for (name, primary, geo) in geometries:
	geo["X"] += offx
	geo["Y"] += offy
	i3_strs.append("{}x{}+{}+{}".format(geo["Width"], geo["Height"], geo["X"], geo["Y"]))
i3_strs

i3config = load_str(i3config_file).strip()
ctx = "# WSLHACKGEN START{}# WSLHACKGEN END"
subre = ctx.format(".*?")
repl =  ctx.format("\nfake-outputs {}\n".format(",".join(i3_strs)))
i3config = re.sub(subre, repl, i3config, flags = re.S)
i3_config = "{}\n".format(i3config)
#print(i3config)

write_str(i3config_file, i3config)



