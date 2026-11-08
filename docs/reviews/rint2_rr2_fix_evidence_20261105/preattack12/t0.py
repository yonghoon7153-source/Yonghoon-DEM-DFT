import time
from harness import *
t0=time.time(); setup(full=True); print('fixtures', round(time.time()-t0,1), 's', T.TD)
d, rc, so = T.led_new('x'); print('led_new rc', rc)
r, n1, so = T.led_add(d, 'ladder:P0'); print('led_add', r, n1)
