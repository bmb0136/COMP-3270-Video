from manim import *
from astar import AStar
from dijkstra import Dijkstra
import os

class Comparison(Scene):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    x = AStar(skip_animations=True)
    y = Dijkstra(skip_animations=True)
    print("Constructing A*")
    x.construct()
    print("Constructing Dijkstra's")
    y.construct()
    self.r_astar = x.result
    self.r_dijkstra = y.result
    self.o_astar = x.visit_order
    self.o_dijkstra = y.visit_order
    print("A", Group(*x.result).width)
    print("D", Group(*y.result).width)
  def construct(self):
    header = Title("Comparison")
    self.add(header)
    self.wait(1)

    d = Group(*self.r_dijkstra).center().shift(RIGHT * 3)
    d_text = Text("Dijkstra's").scale(0.5).move_to(d).align_to(d, UP)
    a = Group(*self.r_astar).center().shift(LEFT * 3)
    a_text = Text("A*").scale(0.5).move_to(a).align_to(d, UP)
    a.shift(DOWN * 0.5)
    d.shift(DOWN * 0.5)
    self.play(AnimationGroup(
      Write(d_text),
      FadeIn(d)
    ))
    self.play(AnimationGroup(
      Write(a_text),
      FadeIn(a)
    ))
    self.wait(1)

    texts = [Tex(*x).scale(0.5).to_edge(DOWN) for x in [
      ["Looking at the final state of Dijkstra's and A*, we can see that A* visited one less node"],
      ["This is because the use of $h(x)$ causes nodes closer to the target to be prioritized"],
      ["For a small graph with $8$ nodes, this advantage seems miniscule"],
      ["But on a larger graph, the difference is clear"],
    ]]
    self.play(Write(texts[0]))
    self.wait(3)

    self.play(ReplacementTransform(texts[0], texts[1]))
    self.wait(3)

    self.play(ReplacementTransform(texts[1], texts[2]))
    self.wait(3)

    self.play(ReplacementTransform(texts[2], texts[3]))
    self.wait(1.5)

    self.play(AnimationGroup(
      FadeIn(img := ImageMobject("compare.png")
             .scale_to_fit_width(14)),
      Write(capt := Text("Source: https://www.youtube.com/watch?v=g024lzsknDo")
            .center()
            .scale(0.5)
            .to_edge(DOWN)
            .add_background_rectangle(buff=SMALL_BUFF)),
      Write(capt2 := Text("Such as here")
            .center()
            .to_edge(UP)
            .shift(DOWN)
            .add_background_rectangle(buff=SMALL_BUFF))
    ))
    self.play(Unwrite(texts[3]))
    self.wait(5)
    self.play(AnimationGroup(
      FadeOut(img),
      Unwrite(capt),
      Unwrite(capt2)
    ))
    self.play(AnimationGroup(
      Unwrite(a_text),
      Unwrite(d_text),
      FadeOut(a),
      FadeOut(d)
    ))
    self.wait(1)

if __name__ == "__main__":
  os.system(f"py -m manim -ql \"{__file__}\" Comparison")