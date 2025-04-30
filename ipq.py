from manim import *
import os

class IPQ(Scene):
  def construct(self):
    header = Title("Indexed Priority Queue")
    self.add(header)
    
    lines = [
      "An Indexed Priority Queue is a combination of a Heap and a Hashmap",
      "that allows for logarithmic time updates to any element's priority"
    ]
    detail = Paragraph(*lines, alignment="center").scale(0.5)
    self.play(Write(detail))
    self.play(detail.animate.move_to(header.get_bottom() + (DOWN * 0.5)))
    self.wait(3)

    heap = MathTable([
      ["A, 1", "Y, 2", "X, 5", "Z, 7", "C, 8", "B, 9"]
    ], include_outer_lines=True).scale(0.5).shift(UP)
    self.play(Create(heap))

    hashmap = MathTable([
      ["A", "B", "C", "X", "Y", "Z"],
      [0, 5, 4, 2, 1, 3]
    ], include_outer_lines=True).scale(0.5).shift(DOWN * 0.5)
    self.play(Create(hashmap))
    self.wait(1)

    detail2 = Paragraph(
      "It functions identically to a normal heap, but the hashmap is used",
      "to lookup the position of each item in the heap. In a normal heap,",
      "this would be linear time instead of constant time.",
    alignment="center").scale(0.5)
    detail2.align_to(detail, UP)
    self.play(ReplacementTransform(detail, detail2))
    self.wait(3)

    steps = [Tex(x).to_edge(DOWN).shift(UP).scale(0.75) for x in [
      "Let's update the key of $Z$ to $0$",
      "Use the hashmap to lookup the position of Z in the heap",
      "Update the key in the heap",
      "$\\text{parent}(Z)=Y$, and $0<2$, so swap $Z$ and $Y$",
      "$\\text{parent}(Z)=Z$, and $0<1$, so swap $Z$ and $A$",
      "$Z$ can no longer be pushed up, so stop"
    ]]
    self.play(Write(steps[0]))
    self.wait(1)

    self.play(ReplacementTransform(steps[0], steps[1]))
    self.wait(1)
    self.play(Succession(
      Indicate(temp1 := hashmap.get_cell((1, 6), color=WHITE)),
      Indicate(temp2 := hashmap.get_cell((2, 6), color=WHITE)),
      Indicate(temp3 := heap.get_cell((1, 4), color=WHITE))
    ))
    self.wait(1)
    
    self.remove(temp1, temp2, temp3)

    self.play(ReplacementTransform(steps[1], steps[2]))
    self.wait(1)
    self.play(AnimationGroup(
      Transform(
        z_old := heap.get_entries((1, 4)),
        z_new := MathTex("Z, 0").move_to(z_old).scale(0.5)
      ),
      Flash(z_new, flash_radius=MED_SMALL_BUFF)
    ))
    self.wait(1)
    self.add(z_new)
    self.remove(z_old)

    self.play(ReplacementTransform(steps[2], steps[3]))
    self.wait(1)
    y = heap.get_entries((1, 2))
    y_pos = hashmap.get_entries((2, 5))
    z_pos = hashmap.get_entries((2, 6))
    self.play(AnimationGroup(
      Swap(y, z_new),
      Swap(y_pos, z_pos)
    ))
    self.wait(1)

    self.play(ReplacementTransform(steps[3], steps[4]))
    self.wait(1)
    a = heap.get_entries((1, 1))
    a_pos = hashmap.get_entries((2, 1))
    self.play(AnimationGroup(
      Swap(a, z_new),
      Swap(a_pos, z_pos)
    ))
    self.wait(1)

    self.play(ReplacementTransform(steps[4], steps[5]))
    self.wait(3)

    self.play(AnimationGroup(
      Unwrite(steps[-1]),
      Unwrite(detail2),
      Uncreate(hashmap),
      Uncreate(heap),
      Uncreate(z_new),
    ))
    self.play(ReplacementTransform(header, Title("Prim's Algorithm")))

if __name__ == "__main__":
  os.system(f"py -m manim -ql \"{__file__}\" IPQ")