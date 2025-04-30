from manim import *
import os

class Dijkstra(Scene):
  def construct(self):
    header = Title("Dijkstra's Algorithm")
    self.add(header)


    self.wait(1)

if __name__ == "__main__":
  os.system(f"py -m manim -ql \"{__file__}\" Dijkstra")