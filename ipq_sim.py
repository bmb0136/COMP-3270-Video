from manim import *

class Sim:
  def __init__(self, scene: Scene, ipq: MathTable, count: int):
    self.scene = scene
    self.ipq = ipq
    self.count = count
    self.id_to_manim = {
      i: ipq.get_entries((1, i + 1))
      for i in range(count)
    }
    self.id_to_idx = {i: i for i in range(count)}
    self.idx_to_id = dict(self.id_to_idx)
    self.keys = {i: float('inf') for i in range(count)}
  
  def decrease_key(self, id, key):
    self.keys[id] = key
    self.scene.play(AnimationGroup(
      Transform(
        old := self.id_to_manim[id],
        new := MathTex(f"{id}, {key}").scale(0.5).move_to(old)
      ),
      Flash(new, flash_radius=MED_SMALL_BUFF)
    ))
    self.scene.remove(old)
    self.scene.add(new)
    self.id_to_manim[id] = new
    while True:
      i = self.id_to_idx[id]
      p = (i - 1) // 2
      if i not in self.idx_to_id or p not in self.idx_to_id:
        break
      if key >= self.keys[self.idx_to_id[p]]:
        break
      self.swap(i, p)
  
  def swap(self, i, j):
    x = self.id_to_manim[self.idx_to_id[i]]
    y = self.id_to_manim[self.idx_to_id[j]]
    self.scene.play(Swap(x, y))
    self.id_to_idx[self.idx_to_id[i]], self.id_to_idx[self.idx_to_id[j]] = \
      self.id_to_idx[self.idx_to_id[j]], self.id_to_idx[self.idx_to_id[i]]
    self.idx_to_id[i], self.idx_to_id[j] = self.idx_to_id[j], self.idx_to_id[i]

  def pop_min(self):
    root_id = self.idx_to_id[0]
    root = self.id_to_manim[root_id]

    self.swap(0, self.count - 1)
    i = 0
    while True:
      L = (2 * i) + 1
      R = (2 * i) + 2
      if L >= self.count - 1 or R >= self.count - 1:
        break

      any = False
      k = self.keys[self.idx_to_id[i]]
      if k > self.keys[self.idx_to_id[L]]:
        self.swap(i, L)
        i = L
        any = True
      
      if k > self.keys[self.idx_to_id[R]]:
        self.swap(i, R)
        i = R
        any = True
      
      if not any:
        break

    self.scene.play(root.animate.center().scale(2))
    self.scene.play(Unwrite(root))

    root_idx = self.id_to_idx[root_id]
    del self.keys[root_id]
    del self.idx_to_id[root_idx]
    del self.id_to_idx[root_id]
    del self.id_to_manim[root_id]
    self.count -= 1
    return root_id
