from manim import *

class End(Scene):
  def construct(self):
    self.play(Write(t := Tex("Video by Brandon Buckley (Spring 2025)")
              .scale(0.75)
              .center()))
    self.wait(2)
    self.play(Unwrite(t))