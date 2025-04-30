from manim import *
from ipq_sim import Sim
from weighted_line import WeightedLine
import os

class Dijkstra(Scene):
  def construct(self):
    header = Title("Dijkstra's Algorithm")
    self.add(header)

    detail = VGroup(*[Tex(*x).scale(0.5) for x in [
      ["Dijkstra's Algorithm finds a minimum cost path on a graph"],
      ["It is nearly identical to Prim's, except that"],
      ["a ", "parent", " node is stored instead of an ", "MST edge"]
    ]]).arrange(DOWN, buff=SMALL_BUFF).center()
    detail[2].set_color_by_tex("MST", YELLOW)
    detail[2].set_color_by_tex("parent", YELLOW)
    self.play(Write(detail))
    self.wait(4)

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
    START = 1
    TARGET = 6

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
    graph.vertices[TARGET].set_color(GREEN)
    graph.vertices[TARGET].submobjects[0].set_color(WHITE)
    graph.shift(RIGHT * 3)
    parents = DiGraph(
      vertices,
      [],
      labels=True,
      layout=graph._layout
    ).scale(0.5).to_corner(DL)
    for o in parents.vertices.values():
      o.submobjects[0].set_color(BLACK)

    distances = {
      k: (MathTex("\\infty")
        .scale(0.5)
        .move_to(x)
        .shift(UL * (x.radius + SMALL_BUFF)), float('inf'))
      for k, x in graph.vertices.items()
    }
    def set_dist(x, val):
      old, _ = distances[x]
      self.play(ReplacementTransform(
        old,
        new := MathTex(f"{val}")
          .scale(0.5)
          .move_to(old)
      ))
      self.remove(old)
      self.add(new)
      distances[x] = (new, val)
    distances[0][0].shift(RIGHT * 0.2)
    distances[2][0].shift(DL * 0.2)
    distances[5][0].shift(DL * 0.2)
    distances[6][0].shift(RIGHT * 0.1)

    ipq = MathTable([[
      f"{i}, \\infty" for i in range(8)
    ]], include_outer_lines=True).scale(0.5)
    ipq.move_to(graph.get_edge_center(DOWN))
    ipq.shift(DOWN * 0.75)
    ipq.to_edge(RIGHT)

    sim = Sim(self, ipq, 8)

    steps = VGroup(*[Tex(*x) for x in [
      ["1. Init IPQ with all nodes with null ", "parent", " and priority $\\infty$"],
      ["2. Initialize nodes with null ", "parent", " and $\\infty$ distance"],
      ["3. Update priority of start node to $0$"],
      ["4. Pop minimum node off IPQ"],
      ["5. If node is target, return path"],
      ["6. Relax adjacent nodes (decrease key and set ", "parent", " if{\\newline}edge weight $<$ key)"],
      ["7. Mark node as ", "seen"],
      ["8. If IPQ is not empty, goto 4"]
    ]]).arrange_in_grid(9, 1, col_alignments="l").scale(0.5).to_edge(LEFT).shift(UP * 1.25)
    steps[0].set_color_by_tex("parent", YELLOW)
    steps[4].set_color_by_tex("parent", YELLOW)
    steps[4].set_color_by_tex("add", RED)
    steps[5].set_color_by_tex("parent", YELLOW)
    steps[6].set_color_by_tex("seen", RED)

    self.play(ReplacementTransform(detail, steps))
    self.remove(detail)
    self.add(steps)
    self.play(Create(graph))
    self.wait(1)

    self.play(Indicate(steps[0]))
    self.play(Create(ipq))
    self.play(Write(Text("IPQ").scale(0.5).move_to(ipq).align_to(ipq, LEFT).shift(LEFT * 0.75)))
    self.wait(1)

    self.play(Indicate(steps[1]))
    self.play(AnimationGroup(
      Write(Text("Parents").scale(0.5).move_to(parents.get_top() + (UP * 0.25))),
      Create(parents),
      AnimationGroup(*[Write(o) for o, _ in distances.values()])
    ))
    self.wait(1)

    self.play(Indicate(steps[2]))
    sim.update_key(START, 0)
    set_dist(START, 0)
    self.wait(1)

    visited = set()
    parent_edges = {}
    while sim.count > 0:
      self.play(Indicate(steps[3]))
      id = sim.pop_min()
      self.wait(1)

      self.play(Indicate(steps[4]))
      if id == TARGET:
        break
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
        if distances[id][1] + w < distances[y][1]:
          sim.update_key(y, w)
          set_dist(y, distances[id][1] + w)
          an = []
          if y in parent_edges:
            an.append(parents.animate.remove_edges(parent_edges[y]))
          an.append(parents.animate.add_edges(
            (y, x),
            edge_type=Arrow
          ))
          parent_edges[y] = (y, x)
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
    
    n = TARGET
    an = []
    while n != START:
      e = parent_edges[n]
      next = e[1]
      if e not in graph.edges:
        e = (e[1], e[0])
      an.append(graph.edges[e].animate.set_stroke(RED))
      n = next
    assert len(an) > 0
    an = an[::-1]
    self.play(Succession(*an))

if __name__ == "__main__":
  os.system(f"py -m manim -ql \"{__file__}\" Dijkstra")