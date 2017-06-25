This is an overview of the tank drive drivetrain model, which was used in one of my blog posts/papers on [my website][1].

Consider both sides of the drivetrain as single wheels, which both have their own velocities. Then, the forwards velocity of the drivetrain is equal to the average of the two velocities.

v_forwards = (v_left + v_right) / 2

However, the drivetrain also has the potential to rotate, by driving the two sides at different velocities. Since when you drive one side backwards and the other side forwards, it goes at its maximum angular velocity, the velocities must be subtracted, not added. Finally, since this calculated velocity is still linear velocity, it can be divided by the robot radius to acquire the robot’s angular velocity.

ω = (v_left − v_right) / r_robot

`model.py` is the model of the drivetrain, applying the equations we just went over.
`unprofiled.py` is a simple PID controller running on the model, controlling both angle and distance.
`profiled.py` generates a trapezoidal motion profile which is then applied to the distance of the drivetrain and driven.
`renderer.py` _hopefully_ renders the movement of the drivetrain when supplied with a csv file. It's not at all guaranteed to work, but it worked on my computer. Have fun resolving dependencies!

[1]:http://steampunc.com
