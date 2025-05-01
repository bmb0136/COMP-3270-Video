import os, sys

scenes = [
  ("intro", "Intro"),
  ("ipq", "IPQ"),
  ("prims", "Prims"),
  ("dijkstra", "Dijkstra"),
  ("astar", "AStar"),
  ("comparison", "Comparison"),
  ("comparison2", "Comparison"),
  ("end", "End"),
]

is_final = "--final" in sys.argv\

codes = (
  os.system(f"py -m manim -q{"h" if is_final else "l"} {script}.py {name}")
  for script, name in scenes
)
for code in codes:
  assert code == 0

folder = "1080p60" if is_final else "480p15"

with open("list", "w") as f:
  f.write("\n".join([f"file '.{os.sep}media{os.sep}videos{os.sep}{script}{os.sep}{folder}{os.sep}{name}.mp4'" for script, name in scenes]))
os.system("ffmpeg -f concat -safe 0 -y -i list -c copy render.mp4")
os.remove("list")
os.system("explorer render.mp4")