import time


class Semaforo:
    def __init__(self, valorInicial=1):
        self.contador = valorInicial


    def acquire(self):
        while True:
            if self.contador > 0:
                self.contador -= 1
                break
            time.sleep(0.01)  # esperar antes de tentar novamente


    def release(self):
        self.contador += 1