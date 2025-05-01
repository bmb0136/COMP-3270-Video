from manim import *
from ipq_sim import Sim
from weighted_line import WeightedLine
import os, math

class AStar(Scene):
  def construct(self):
    header = Title("A*")
    self.add(header)
    self.wait(1)

    detail = VGroup(*[Tex(*x).scale(0.75) for x in [
      ["A* finds a minimum cost path on a graph"],
      ["It is nearly identical to Dijkstra's, except:"],
      ["$\\cdot$ a ", "score", " is stored for each node in addition to the ", "distance"],
      ["$\\cdot$ a heuristic function $h(x)$ that returns a lower{\\newline}bound on the distance to the target*"],
      ["*This is typically Euclidean distance"]
    ]]).arrange(DOWN, buff=SMALL_BUFF).center()
    detail[2].set_color_by_tex("score", ORANGE)
    detail[2].set_color_by_tex("dist", BLUE)
    detail[3]
    self.play(Write(detail))
    self.wait(8)

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

    data = {
      k: (VGroup(
          MathTex("\\infty").set_color(BLUE),
          Circle(SMALL_BUFF).set_color(BLACK),
          MathTex("\\infty").set_color(ORANGE)
        )
        .arrange(buff=0)
        .scale(0.5)
        .move_to(x)
        .shift(UL * (x.radius + SMALL_BUFF)), float('inf'), float('inf'))
      for k, x in graph.vertices.items()
    }
    def set_data(x, val, score):
      old, _, _ = data[x]
      self.play(ReplacementTransform(
        old,
        new := VGroup(
            MathTex(f"{val}").set_color(BLUE),
            Circle(SMALL_BUFF).set_color(BLACK),
            MathTex(f"{score:.1f}").set_color(ORANGE)
          )
        .arrange(buff=0)
          .scale(0.5)
          .move_to(old)
      ))
      self.remove(old)
      self.add(new)
      new[0].set_color(BLUE)
      new[2].set_color(ORANGE)
      data[x] = (new, val, score)
    data[0][0].shift(RIGHT * 0.3)
    data[2][0].shift(DL * 0.2)
    data[5][0].shift(DL * 0.25)
    data[3][0].shift(LEFT * 0.2)
    data[6][0].move_to(graph.vertices[6]) \
      .shift(DOWN * ((graph.vertices[6]).radius + 0.15))
    
    h = lambda x: (lambda a, b: math.sqrt(sum((
      math.pow(a[i] - b[i], 2)
      for i in range(3)
    ))))(graph._layout[x], graph._layout[TARGET])

    ipq = MathTable([[
      f"{i}, \\infty" for i in range(8)
    ]], include_outer_lines=True).scale(0.5)
    ipq.move_to(graph.get_edge_center(DOWN))
    ipq.shift(DOWN * 0.75)
    ipq.to_edge(RIGHT)

    sim = Sim(self, ipq, 8)

    steps = VGroup(*[Tex(*x) for x in [
      ["1. Init IPQ with all nodes with $\\infty$ priority"],
      ["2. Initialize nodes with null ", "parent", ", $\\infty$\\space", " distance ", ", and $\\infty$\\space", " score"],
      ["3. Update ", "distance", " of start node to $0$, and ", "priority", " to $h(x)$"],
      ["4. Pop minimum node off IPQ"],
      ["5. If node is target, return path (reversed parent chain)"],
      ["6. Relax adjacent nodes (decrease key, set ", "parent", ", update ", "distance", ",{\\newline} and update ", "score", " if adj.", "dist", " $+$ weight $<$ current.", "dist", ")"],
      ["7. Mark node as ", "seen"],
      ["8. If IPQ is not empty, goto 4"]
    ]]).arrange_in_grid(9, 1, col_alignments="l").scale(0.5).to_edge(LEFT).shift(UP * 1.15)
    steps[1].set_color_by_tex("dist", BLUE)
    steps[1].set_color_by_tex("score", ORANGE)
    steps[2].set_color_by_tex("dist", BLUE)
    steps[4].set_color_by_tex("parent", YELLOW)
    steps[4].set_color_by_tex("add", RED)
    steps[5].set_color_by_tex("parent", YELLOW)
    steps[5].set_color_by_tex("dist", BLUE)
    steps[5].set_color_by_tex("score", ORANGE)
    steps[6].set_color_by_tex("seen", RED)

    self.play(ReplacementTransform(detail, steps))
    self.remove(detail)
    self.add(steps)
    self.play(Create(graph))
    self.wait(1)

    self.play(Indicate(steps[0]))
    self.play(Create(ipq))
    self.play(Write(ipq_text := Text("IPQ").scale(0.5).move_to(ipq).align_to(ipq, LEFT).shift(LEFT * 0.75)))
    self.wait(1)

    self.play(Indicate(steps[1]))
    self.play(AnimationGroup(
      Write(parents_text := Text("Parents").scale(0.5).move_to(parents.get_top() + (UP * 0.25))),
      Create(parents),
      AnimationGroup(*[Write(o) for o, _, _ in data.values()])
    ))
    self.wait(1)

    self.play(Indicate(steps[2]))
    sim.update_key(START, h(START))
    set_data(START, 0, h(START))
    self.wait(1)

    visited = set()
    self.visit_order = []
    parent_edges = {}
    highlight = Circle(
      graph.vertices[0].radius + (SMALL_BUFF / 2),
      color=PURPLE
    )
    while sim.count > 0:
      self.play(Indicate(steps[3]))
      id = sim.pop_min()
      if sim.count == len(vertices) - 1: # first
        self.play(GrowFromCenter(highlight.move_to(graph.vertices[id])))
      else:
        self.play(highlight.animate.move_to(graph.vertices[id]))
      self.visit_order.append(id)
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
        if y in visited:
          continue
        self.play(Indicate(graph.vertices[y]))
        w = graph.edges[e].weight
        if data[id][1] + w < data[y][1]:
          dist = data[id][1] + w
          set_data(y, dist, dist + h(y))
          sim.update_key(y, data[y][2])
          an = []
          if y in parent_edges:
            an.append(parents.animate.remove_edges(parent_edges[y]))
          an.append(parents.animate.add_edges(
            (y, x),
            edge_type=Arrow,
            edge_config={"color": YELLOW}
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
    self.play(AnimationGroup(*an))

    self.result = [graph.copy()] + [x[0].copy() for x in data.values()]

    self.wait(3)
    self.play(AnimationGroup(
      Uncreate(graph),
      Uncreate(ipq),
      Uncreate(parents),
      ShrinkToCenter(highlight),
      Unwrite(steps),
      Unwrite(parents_text),
      Unwrite(ipq_text),
      AnimationGroup(*[Unwrite(x) for x in sim.id_to_manim.values()]),
      AnimationGroup(*[Unwrite(x) for x, _, _ in data.values()])
    ))
    self.play(ReplacementTransform(header, Title("Comparison")))
    self.wait(1)

if __name__ == "__main__":
  os.system(f"py -m manim -ql \"{__file__}\" AStar")