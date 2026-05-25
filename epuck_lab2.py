"""epuck_lab2 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import math

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# MOTORES
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# SENSORES DE DISTANCIA
sensor_names = ['ps0', 'ps7', 'ps5', 'ps2']
sensors = []

for name in sensor_names:
    s = robot.getDevice(name)
    s.enable(timestep)
    sensors.append(s)
    
# ENCODERS
left_encoder = robot.getDevice('left wheel sensor')
right_encoder = robot.getDevice('right wheel sensor')

left_encoder.enable(timestep)
right_encoder.enable(timestep)

# VARIABLES DE FILTRO SIMPLE
filtered_front = 0
alpha = 0.3

# VARIABLES KALMAN
estimated_distance = 0
P = 1
Q = 0.01
R = 5

prev_left = 0
prev_right = 0

# Variables movimiento
turning = False
turn_steps = 0
turn_direction = 0
stuck_steps = 0

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # LEER SENSORES
    front_right = sensors[0].getValue()
    front_left = sensors[1].getValue()

    left_side = sensors[2].getValue()
    right_side = sensors[3].getValue()

    front_distance = (front_right + front_left) / 2


    # FILTRO SIMPLE
    filtered_front = alpha * front_distance + (1 - alpha) * filtered_front

    # ENCODERS 
    left_pos = left_encoder.getValue()
    right_pos = right_encoder.getValue()

    delta_left = left_pos - prev_left
    delta_right = right_pos - prev_right

    prev_left = left_pos
    prev_right = right_pos

    # avance aproximado
    delta_movement = (delta_left + delta_right) / 2

    # KALMAN 

    # prediccion
    predicted_distance = estimated_distance - delta_movement
    P = P + Q

    # ganancia
    K = P / (P + R)

    # correccion
    estimated_distance = predicted_distance + K * (filtered_front - predicted_distance)

    # actualizar covarianza
    P = (1 - K) * P

    # NAVEGACION 
    threshold = 80
    
    if turning:
    
        turn_steps -= 1
    
        # mantener direccion elegida
        if turn_direction == 1:
            # derecha
            left_motor.setVelocity(4)
            right_motor.setVelocity(1)
            print("Girando derecha")
    
        else:
            # izquierda 
            left_motor.setVelocity(1)
            right_motor.setVelocity(4)
            print("Girando izquierda")
    
        # terminar giro
        if turn_steps <= 0:
            turning = False
    
    else:
    
        # camino libre
        if estimated_distance < threshold:
        
            # intentar avanzar
            left_motor.setVelocity(4)
            right_motor.setVelocity(4)
        
            print("Avanza")
        
            # verificar si realmente se movio
            movement = abs(delta_movement)
        
            if movement < 0.001:
                stuck_steps += 1
            else:
                stuck_steps = 0
        
            # si esta atrapado mucho tiempo
            if stuck_steps > 20:
        
                print("ATORADO")
        
                turning = True
                turn_steps = 30
        
                # girar hacia lado mas libre
                if left_side > right_side:
                    turn_direction = 1
                else:
                    turn_direction = -1
        
                stuck_steps = 0
    
        else:
    
            print("Obstaculo detectado")
    
            left_motor.setVelocity(-2)
            right_motor.setVelocity(-2)
            
            for _ in range(5):
                robot.step(timestep)
            
            # activar modo giro
            turning = True
    
            # cuanto tiempo girar
            turn_steps = 25
    
            # elegir direccion SOLO UNA VEZ
            if left_side > right_side:
                turn_direction = 1
            else:
                turn_direction = -1


# ANTIGUO
    # if estimated_distance < threshold:
        # avanzar
        # left_motor.setVelocity(4)
        # right_motor.setVelocity(4)
        # print("avanza")

    # else:
        # obstaculo detectado

        # if left_side > right_side:
            # girar derecha
            # left_motor.setVelocity(3)
            # right_motor.setVelocity(-3)
            # print("Derecha")

        # else:
            # girar izquierda
            # left_motor.setVelocity(-3)
            # right_motor.setVelocity(3)
            # print("izquierda")


    # DEBUG
    print("Frente:", front_distance)
    print("Filtrado:", filtered_front)
    print("Estimado:", estimated_distance)

# Enter here exit cleanup code.
