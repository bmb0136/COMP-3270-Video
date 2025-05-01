from manim import *
import os

class Intro(Scene):
  def construct(self):
    header = Title("Prim's, Dijkstra's, and A*")
    self.play(Write(header))

    intro = Paragraph(
      "Prim's Algorithm returns an MST for a given graph",
      "",
      "It is asymptotically faster than Kruskal's",
      "",
      "Prim's primary advantage is the use of an Indexed Priority Queue",
      "",
      "Prim's is closely related to Dijkstra's Algorithm and A*;",
      "the differences between them are only a few lines of code",
      alignment="center"
    ).scale(0.5).center()
    ipq_pos = 2 - len("Indexed Priority Queue")
    intro[4][ipq_pos:].color = YELLOW
    self.play(Write(intro))

    self.wait(4)
    self.play(LaggedStart(*[
      Unwrite(intro[0]),
      Unwrite(intro[2]),
      Unwrite(VGroup(intro[4][:ipq_pos])),
      Unwrite(intro[6]),
      Unwrite(intro[7]),
      intro[4][ipq_pos:].animate.move_to(ORIGIN),
      Unwrite(header)
    ], lag_ratio=0.5))
    self.play(ReplacementTransform(intro[4][ipq_pos:], Title("Indexed Priority Queue")))

if __name__ == "__main__":
  os.system(f"py -m manim -ql \"{__file__}\" Intro")