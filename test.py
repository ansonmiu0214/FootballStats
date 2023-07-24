import matplotlib.pyplot as plt

from mplsoccer import Pitch, VerticalPitch

pitch = Pitch()
# specifying figure size (width, height)
fig, ax = pitch.draw(figsize=(8, 4))

plt.show()
