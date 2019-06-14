---
title: Controls!
author: Finn Boire
...

---

# Robot Controls!


---

# Proportional Control

We have an error, and we want to respond to that error based off of its
magnitude.

```
error = (goal - current_state)

input = kP * error
```

---

# No friction

---

# Derivative Control

Look at how quickly the thing is changing, and make something proportional to the rate of change.

```
error = (goal - current_state)
derivative = (current_state - previous_state) / time_step
previous_state = current_state
input = kP * error + kD * derivative
```
---

# Constant forces

---

# Integral Control

We want it to respond to error if it persists over time.

```
error = (goal - current_state)
derivative = (current_state - previous_state) / time_step
previous_state = current_state
integral += error / time_step
input = kP * error + kD * derivative + kI * integral
```

---

# More demos! Ask questions!
