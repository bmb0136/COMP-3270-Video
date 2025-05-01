from manim import *
import os

class Comparison(Scene):
  def construct(self):
    header = Title("Comparison")
    self.add(header)
    self.wait(1)

    table = MobjectTable([
      [
        Tex("Algorithm"),
        Tex("Node Data"),
        Tex("Relax Condition"),
        Tex("Relax Action"),
        Tex("Initial\\\\Priority"),
        Tex("Returns")
      ],
      [
        Tex("Prim's"),
        Tex("MST Edge\\\\", "MST Weight")
          .set_color_by_tex("Edge", YELLOW)
          .set_color_by_tex("Weight", BLUE),
        Tex("e.weight $<$ adj.", "mst\\_weight")
          .set_color_by_tex("mst", BLUE),
        Tex("mst\\_edge", " = e\\\\", "updateKey(adj, e.weight)")
          .set_color_by_tex("edge", YELLOW),
        Tex("0"),
        Tex("MST")
      ],
      [
        Tex("Dijkstra's"),
        Tex("Parent\\\\", "Distance")
          .set_color_by_tex("Parent", YELLOW)
          .set_color_by_tex("Dist", BLUE),
        Tex("curr.", "dist", " $<$ e.weight $+$ adj.", "dist")
          .set_color_by_tex("dist", BLUE),
        Tex("parent = e\\\\updateKey(adj,\\\\curr.", "dist", " $+$ e.weight)")
          .set_color_by_tex("dist", BLUE),
        Tex("0"),
        Tex("Path")
      ],
      [
        Tex("A*"),
        Tex("Parent\\\\", "Distance\\\\", "Score")
          .set_color_by_tex("Parent", YELLOW)
          .set_color_by_tex("Dist", BLUE)
          .set_color_by_tex("Score", ORANGE),
        Tex("curr.", "dist", " $+$ e.weight $<$ adj.", "dist")
          .set_color_by_tex("dist", BLUE),
        Tex("parent = e\\\\updateKey(adj,\\\\curr.", "dist", " $+$ e.weight\\\\$+$ ", "h(adj)", ")")
          .set_color_by_tex("h(adj)", ORANGE)
          .set_color_by_tex("dist", BLUE),
        MathTex("h(x)").set_color(ORANGE),
        Tex("Path")
      ],
    ], include_outer_lines=True).scale(0.4).to_edge(DOWN)

    text_pos = (header.get_bottom() + table.get_top()) / 2
    texts = [Tex(*x).scale(0.75).move_to(text_pos) for x in [
      ["All three algorithms can be summarized as follows"],
      ["Barring A*'s initial priority and the return values, the relax step and data are the only differences"],
      ["Implementation wise, all three add the nodes to an IPQ, pop the minimum, and relax adjacent edges/nodes"],
      ["In fact, A* and Dijkstra's are so similar that A* is equivalent to Dijkstra's if $h(x)=0$"],
      ["Conversely, Dijkstra is equivalent to A* if $h(u)-h(v)$ is added to each edge $(u,v)$"],
      ["Lastly, Prim's and Dijkstra's are only different by the distance/weight values assigned to each node and the return value"],
    ]]

    self.play(Write(texts[0]))

    self.play(Write(table))
    self.wait(2)

    for i in range(1, len(texts)):
      self.play(ReplacementTransform(texts[i - 1], texts[i]))
      self.wait(5)
    
    self.play(Unwrite(texts[-1]))
    self.play(Unwrite(table))
    self.play(Unwrite(header))
    self.wait(1)

if __name__ == "__main__":
  os.system(f"py -m manim -ql \"{__file__}\" Comparison")