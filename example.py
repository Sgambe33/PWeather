from datetime import *
from pivottablejs import pivot_ui
import utils
from meteostat import *
start = datetime.now() - timedelta(hours=24)
end = datetime.now()
data = Hourly('72219', start, end )
data = data.fetch() 
print(type(data))
pivot_ui(data)

