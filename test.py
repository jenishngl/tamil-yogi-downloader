from progress.bar import Bar
import time

TEST = 431
bar= Bar()

time.sleep(5)
bar = Bar('Processing', max=TEST)
bar.next()
for _ in range(TEST):
    time.sleep(0.1)
    bar.next()

bar.finish()