from atomos.atomic import AtomicReference
# ref https://github.com/maxcountryman/atomos


class ListenerHolder():
    def __init__(self):
        self.value = None

    def set(self,value):
        self.value = AtomicReference(value)

    def get(self):
        return self.value.get()

if __name__ == '__main__':
    from distrilockper.util.Runnable import Runnable

    def run():
        a = 1 + 1


    state = ListenerHolder()
    state.set(Runnable(run))
    #print(state.get())