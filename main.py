import os, sys, subprocess

scenes = [
  ("intro", "Intro"),
  ("ipq", "IPQ"),
  ("prims", "Prims"),
  ("dijkstra", "Dijkstra"),
  ("astar", "AStar")
]

is_final = "--final" in sys.argv

for script, name in scenes:
  assert os.system(f"py -m manim -ql -s {script}.py {name}") == 0

proc_list = [subprocess.Popen([
  "py",
  "-m",
  "manim",
  f"-q{"h" if is_final else "l"}",
  f"{script}.py",
  name
]) for script, name in scenes]
for p in proc_list:
  p.wait()

folder = "1080p60" if is_final else "480p15"

with open("list", "w") as f:
  f.write("\n".join([f"file '.{os.sep}media{os.sep}videos{os.sep}{script}{os.sep}{folder}{os.sep}{name}.mp4'" for script, name in scenes]))
os.system("ffmpeg -f concat -safe 0 -y -i list -c copy render.mp4")
os.remove("list")