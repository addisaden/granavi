# granavi

```python
from granavi import Node

class Rail(Node):
	def __init__(self, name, raillength=1, description=""):
		super().__init__(name, description)
		self.raillength = raillength
	
class Station(Node):
	pass
	
station_a = Station("Station A")
station_b = Station("Station B")
station_c = Station("Station C")

rail_a_b = Rail("A -> B", 5)
[rail_a_b.connect(i, bidirect=True) for i in [station_a, station_b]]

rail_b_c = Rail("B -> C", 3)
for i in [station_b, station_c]:
	rail_b_c.connect(i, bidirect=True)

result = 0
for i in station_a.pathTo(station_c):
	if isinstance(i, Rail):
		result += i.raillength
```
