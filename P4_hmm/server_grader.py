lines = []
with open('results.txt', 'r') as f:
    lines = f.readlines()

start, end = None, None

for i in reversed(range(len(lines))):
	if lines[i].startswith("Total: ") and lines[i-1].strip() == "------------------":
		end = i - 1
		continue
	if lines[i].strip() == "==================" and lines[i-1].strip() == "Provisional grades":
		start = i + 1
		break

lines = lines[start: end]
# print lines
s = [int(l.split()[2].split('/')[0]) for l in lines]
scores = "\"scores\": {" + ', '.join([('\"q%d\": '%(i+1)) + str(x) for i, x in enumerate(s)]) + "}"

s.append(sum(s))
scoreboard = "\"scoreboard\": [" + ', '.join(str(x) for x in s) + "]" 

print("{" + scores + ", " + scoreboard + "}")
