from hub import light_matrix, port, sound
import runloop, motor, motor_pair, distance_sensor, random, color_sensor



# ------------------------
# Movement functions
# -----------------

async def leftTurn(desiredAngle):
    """ A custom function for making the robot turn to a desired angle to the left whilst on the spot
    Input: desiredAngle = The amount you want to turn in degrees
    """
    motorDegrees = desiredAngle * 2

    motor.run_for_degrees(port.C, motorDegrees, 360)
    await motor.run_for_degrees(port.D, motorDegrees, 360)

async def rightTurn(desiredAngle):
    """ A custom function for making the robot turn to a desired angle to the right whilst on the spot
    Input: desiredAngle = The amount you want to turn in degrees
    """
    motorDegrees = desiredAngle * 2

    motor.run_for_degrees(port.C, motorDegrees, -360)
    await motor.run_for_degrees(port.D, motorDegrees, -360)


# ------------------------
# Dancing functions
# ------------------------

# TO-DO


async def main():

    # Variables
    runtime = runloop.time()
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.D) # Links the wheels to eachother for easier movement
    wheels = motor_pair.PAIR_1 # Rebind the PAIR_1 to wheels for easier calling

    # Line follower settings
    baseSpeed = 360
    turnStrength = 2.5


    while True: # Main function when running
        distance = distance_sensor.distance(port.F)


        # ------------------------
        # Distance/End Detection
        # ------------------------

        if distance != -1 and distance <= 100: # Checks when the robot is closer than 10cm to an object and isn't reading -1 (out of range)
            motor_pair.stop(wheels)
            await sound.beep(440, 500, 100)

            await runloop.sleep_ms(10)
            break

        # ------------------------
        # Read color sensors
        # ------------------------

        colorLeft = color_sensor.reflection(port.A)
        colorRight = color_sensor.reflection(port.B)

        # ------------------------
        # Line following
        # ------------------------

        error = colorLeft - colorRight # Finds difference in amount of black found by the sensors 
        steering = int(error * turnStrength) # Converts the error into an amount of turn force and is multiplied by the turn strength variable 

        steering = max(-100, min(100, steering)) # Keeps the turn force within accepted limits -100 to 100

        motor_pair.move(wheels, steering, velocity=baseSpeed) # Moves the robot forward and turns based on how much black is showed to the sensors


        # ------------------------
        # Testers
        # ------------------------

        print(colorLeft, colorRight, error, steering)

        # print(f"Color left = {colorLeft}, Color right = {colorRight}, difference = {error}, turn force = {steering}")

        await runloop.sleep_ms(10)




runloop.run(main())