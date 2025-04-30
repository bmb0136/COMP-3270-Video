from manim import *
from WeightedLine import WeightedLine
from ipq_sim import Sim
import os

class Prims(Scene):
  def construct(self):
    header = Title("Prim's Algorithm")
    self.add(header)

    vertices = list(range(8))
    edges = [
      (0, 1, 10),
      (0, 2, 1),
      (0, 3, 4),
      (1, 2, 3),
      (1, 4, 0),
      (2, 5, 8),
      (2, 3, 2),
      (3, 5, 2),
      (3, 6, 7),
      (4, 5, 1),
      (4, 7, 8),
      (5, 6, 6),
      (5, 7, 9),
      (6, 7, 12)
    ]

    graph = Graph(
      vertices,
      [(x, y) for x, y, _ in edges],
      labels=True,
      layout="kamada_kawai",
      edge_type=WeightedLine,
      edge_config={(x, y): {"weight": z} for x, y, z in edges}
    )
    for o in graph.vertices.values():
      o.submobjects[0].set_color(BLACK)
    graph.shift(RIGHT * 3)
    mst = Graph(
      vertices,
      [(x, y) for x, y, _ in edges],
      labels=True,
      layout="kamada_kawai"
    ).scale(0.5).to_corner(DL)
    for o in mst.vertices.values():
      o.submobjects[0].set_color(BLACK)
    for o in mst.edges.values():
      o.set_color(BLACK)

    ipq = MathTable([[
      f"{i}, \\infty" for i in range(8)
    ]], include_outer_lines=True).scale(0.5)
    ipq.move_to(graph.get_edge_center(DOWN))
    ipq.shift(DOWN * 0.75)
    ipq.to_edge(RIGHT)

    sim = Sim(self, ipq, 8)

    steps = VGroup(*[Tex(*x) for x in [
      ["1. Init IPQ with all nodes with null MST edge and priority $\\infty$"],
      ["2. Create MST with no edges"],
      ["3. Update priority of start node to $0$"],
      ["4. Pop minimum node off IPQ"],
      ["5. If the node's ", "MST edge", " is not null, ", "add", " to MST"],
      ["6. Relax adjacent nodes"],
      ["7. Mark node as ", "seen"],
      ["8. If IPQ is not empty, goto 4"]
    ]]).arrange_in_grid(8, 1, col_alignments="l").scale(0.5).to_edge(LEFT).shift(UP * 1.25)

    steps[4].set_color_by_tex("MST edge", YELLOW)
    steps[4].set_color_by_tex("add", RED)

    steps[6].set_color_by_tex("seen", RED)

    self.play(Write(steps))
    self.play(Create(graph))
    self.wait(1)

    self.play(Indicate(steps[0]))
    self.play(Create(ipq))
    self.play(Write(Text("IPQ").scale(0.5).move_to(ipq).align_to(ipq, LEFT).shift(LEFT * 0.75)))
    self.wait(1)

    self.play(Indicate(steps[1]))
    self.play(AnimationGroup(
      Write(Text("MST").scale(0.5).move_to(mst.get_top() + (UP * 0.25))),
      Create(mst)
    ))
    self.wait(1)

    self.play(Indicate(steps[2]))
    sim.update_key(1, 0)
    self.wait(1)

    visited = set()
    mst_edges = {}
    mst_weight = {x: sim.keys[x] for x in graph.vertices.keys()}
    while sim.count > 0:
      self.play(Indicate(steps[3]))
      id = sim.pop_min()
      self.wait(1)

      self.play(Indicate(steps[4]))
      self.play(Indicate(mst.vertices[id]))
      if id in mst_edges:
        x, y = mst_edges[id]
        e = mst.edges[(x, y)]
        self.play(AnimationGroup(
          e.animate.set_color(RED),
          Flash(e, flash_radius=MED_SMALL_BUFF)
        ))
      self.wait(1)
      
      self.play(Indicate(steps[5]))
      adjacent = (
        k
        for k in graph.edges.keys()
        if id in k
      )
      for x, y in adjacent:
        e = (x, y)
        if x != id:
          x, y = y, x
        self.play(Indicate(graph.vertices[y]))
        if y in visited:
          continue
        w = graph.edges[e].weight
        if w < mst_weight[y]:
          sim.update_key(y, w)
          mst_weight[y] = w
          an = [mst.edges[e].animate.set_color(YELLOW)]
          if y in mst_edges:
            an.append(mst.edges[mst_edges[y]].animate.set_color(BLACK))
          mst_edges[y] = e
          self.play(AnimationGroup(*an))
      self.wait(1)

      self.play(Indicate(steps[6]))
      self.play(AnimationGroup(
        Flash(graph.vertices[id], flash_radius=graph.vertices[id].radius + SMALL_BUFF),
        graph.vertices[id].animate.set_color(RED),
        graph.vertices[id].submobjects[0].animate.set_color(WHITE),
      ))
      visited.add(id)
      self.wait(1)

      self.play(Indicate(steps[7]))

    self.play(LaggedStart(*[
      graph.edges[e].animate.set_stroke(RED)
      for e, v in mst.edges.items()
      if v.color == RED
    ]))
    self.wait(1)

if __name__ == "__main__":
  os.system(f"py -m manim -ql \"{__file__}\" Prims")