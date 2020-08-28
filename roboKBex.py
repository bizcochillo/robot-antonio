class Robot:
    def __init__(self):
        try:
            import RPi.GPIO as GPIO
        except RuntimeError:
            print("Error importing RPi.GPIO!  This must be run as root using sudo")
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        #I-B: Iquierda para detras
        self.GPIO.setup(17, GPIO.OUT)
        #I-F. Iquierda para adelante
        self.GPIO.setup(18, GPIO.OUT)
        #D-B Derecha para atras
        self.GPIO.setup(22, GPIO.OUT)
        #Derecha para adelante
        self.GPIO.setup(23, GPIO.OUT)


    def up(self):
        self.GPIO.output(17, False)
        self.GPIO.output(18, True)
        self.GPIO.output(22, False)
        self.GPIO.output(23, True)


    def back(self):
        self.GPIO.output(17, True)
        self.GPIO.output(18, False)
        self.GPIO.output(22, True)
        self.GPIO.output(23, False)

    def left(self):
        self.GPIO.output(17, False)
        self.GPIO.output(18, True)
        self.GPIO.output(22, False)
        self.GPIO.output(23, False)

    def right(self):
        self.GPIO.output(17, False)
        self.GPIO.output(18, False)
        self.GPIO.output(22, False)
        self.GPIO.output(23, True)


    def stop(self):
        self.GPIO.output(17, False)
        self.GPIO.output(18, False)
        self.GPIO.output(22, False)
        self.GPIO.output(23, False)
    def getch(self):
        import sys, tty, termios
        old_settings = termios.tcgetattr(0)
        new_settings = old_settings[:]
        new_settings[3] &= ~termios.ICANON
        try:
            termios.tcsetattr(0, termios.TCSANOW, new_settings)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(0, termios.TCSANOW, old_settings)
        return ch

robot = Robot();
while True:
    print("Adelante: E. ");
    print("Atras:    C.");
    print("Iquierda: S.");
    print("Derecha:  F.");
    print("Fin: P");
    nb = robot.getch();
    if nb == b'E' or nb == b'e':
        print("Adelante\n");
        robot.adelante();
    elif nb == b'c' or nb == b'C':
        print("Atras\n");
        robot.atras();
    elif nb == b'S' or nb == b's':
        print("Iquierda\n");
        robot.izquierda();
    elif nb == b'F' or nb == b'f':
        print("Derecha\n");
        robot.derecha()
    elif nb == b'p' or nb == b'P':
        print("Fin\n");
        robot.parar();
        break
