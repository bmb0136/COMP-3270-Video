from manim import *
from ipq_sim import Sim
from weighted_line import WeightedLine
import os

class AStart(Scene):
  def construct(self):
    header = Title("A*")
    self.add(header)
    self.wait(1)

if __name__ == "__main__":
  os.system(f"py -m manim -ql \"{__file__}\" AStar")