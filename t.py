import maya

a1 = maya.now()
a2 = a1.add(hours=1)

i = maya.MayaInterval(a1, a2)
print i