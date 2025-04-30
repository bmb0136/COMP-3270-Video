from manim import *
import os

class Intro(Scene):
  def construct(self):
    header = Title("Prim's, Dijkstra's, and A*")
    self.play(Write(header))

    intro = Paragraph(
      "Prim's Algorithm converts a graph into a MST",
      "It is asymptotically faster than Kruskal's",
      "Prim's primary advantage is the use of an Indexed Priority Queue",
      alignment="center"
    ).scale(0.5)
    ipq_pos = 2 - len("Indexed Priority Queue")
    intro[2][ipq_pos:].color = YELLOW
    self.play(Write(intro))

    self.wait(4)
    self.play(LaggedStart(
      Unwrite(VGroup(intro[0], intro[1], intro[2][:ipq_pos])),
      intro[2][ipq_pos:].animate.move_to(ORIGIN),
      Unwrite(header),
      lag_ratio=0.5
    ))
    self.play(ReplacementTransform(intro[2][ipq_pos:], Title("Indexed Priority Queue")))

if __name__ == "__main__":
  os.system(f"py -m manim -ql \"{__file__}\" Intro")