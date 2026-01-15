from gpiozero import Motor
from time import sleep
FL = Motor(forward=27, backward=17)
FR = Motor(forward=6, backward=5)
RL = Motor(forward=23,  backward=22)
RR = Motor(forward=19, backward=13)

motors = [FL, FR, RL, RR]

def stop_all():
    for m in motors:
        m.stop()

def set_motor(m: Motor, value: float):
    if value > 0:
        m.forward(value)
    elif value < 0:
        m.backward(-value)
    else:
        m.stop()

def normalize(fl, fr, rl, rr):
    mx = max(abs(fl), abs(fr), abs(rl), abs(rr), 1.0)
    return fl/mx, fr/mx, rl/mx, rr/mx

def mecanum(vx, vy, w):
    fl = vx - vy - w
    fr = vx + vy + w
    rl = vx + vy - w
    rr = vx - vy + w
    return normalize(fl, fr, rl, rr)

def drive(vx, vy, w, speed=1.0):
    fl, fr, rl, rr = mecanum(vx, vy, w)
    set_motor(FL, fl * speed)
    set_motor(FR, fr * speed)
    set_motor(RL, rl * speed)
    set_motor(RR, rr * speed)

print("w: forward | s: backward | a: strafe left | d: strafe right")
print("j: rotate left | l: rotate right | q: stop | e: exit")

try:
    while True:
        cmd = input("cmd: ").lower().strip()

        if cmd == 'w':
            drive( 1, 0, 0, speed=0.8)
        elif cmd == 's':
            drive(-1, 0, 0, speed=0.8)
        elif cmd == 'a':
            drive( 0,-1, 0, speed=0.8)
        elif cmd == 'd':
            drive( 0, 1, 0, speed=0.8)
        elif cmd == 'j':
            drive( 0, 0,-1, speed=0.7)
        elif cmd == 'l':
            drive( 0, 0, 1, speed=0.7)
        elif cmd == 'q':
            stop_all()
        elif cmd == 'e':
            stop_all()
            break
        else:
            print("unknown")

except KeyboardInterrupt:
    stop_all()