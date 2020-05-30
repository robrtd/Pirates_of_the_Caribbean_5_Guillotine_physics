import numpy as np
import matplotlib.pyplot as plt


class Pendulum:
    def __init__(self, phi_0, phi_1):
        self.phi_0 = [phi_0]
        self.phi_1 = [phi_1]
        self.dt = 0.01
        self.g = 9.81
        self.r = 1

    def update(self, do_rotate=True):
        if do_rotate:
            phi_1 = self.phi_1[-1] + self.g/self.r*np.sin(self.phi_0[-1]) * self.dt
            phi_0 = self.phi_0[-1] + phi_1 * self.dt
        else:
            phi_1 = self.phi_1[-1]
            phi_0 = self.phi_0[-1]
        self.phi_1.append(phi_1)
        self.phi_0.append(phi_0)

    def __str__(self):
        return f'{self.phi_0[-1]}, {self.phi_1[-1]}'


class Knife:
    def __init__(self, l, p: Pendulum, L=None):
        self.pendulum = p
        self.alpha = p.phi_0[-1]
        self.L = l if L is None else L
        self.l_start = l
        self.l_0 = [L]
        self.l_1 = [0.0]
        self.rotation_started = False

    def get_knife_pos(self):
        alpha = self.alpha
        pos_x = [-l*np.sin(phi-alpha) for l, phi in zip(self.l_0, self.pendulum.phi_0)]
        pos_y = [l*np.cos(phi-alpha) for l, phi in zip(self.l_0, self.pendulum.phi_0)]
        return pos_x, pos_y

    def update(self):
        if self.rotation_started or self.l_0[-1] <= self.l_start:
            self.rotation_started = True
        self.pendulum.update(self.rotation_started)
        l_1 = self.l_1[-1] + \
              (-self.pendulum.g * np.cos(self.pendulum.phi_0[-1]-self.alpha) +
               self.l_0[-1] * (self.pendulum.phi_1[-1])**2) * \
              self.pendulum.dt
        l_0 = self.l_0[-1] + l_1 * self.pendulum.dt

        # boundary condition 1
        if l_0 > self.L:
            print("b1")
            l_0 = self.L
            l_1 = 0

        # boundary condition 2
        if l_0 < 0:
            print(f"Now you die! Knifespeed: {l_1}")
            l_0 = .0
            l_1 = .0
        self.l_1.append(l_1)
        self.l_0.append(l_0)

    def __str__(self):
        return f'{self.l_0[-1]}, {self.l_1[-1]}'


p = Pendulum(np.pi/3, 0.0)
k = Knife(l=3.0, p=p, L=4.)
for t in range(600):
    k.update()
    print(k, p)

plt.plot(p.phi_0)
plt.plot(p.phi_1)
plt.plot(k.l_0)
plt.show()
pos_x, pos_y = k.get_knife_pos()
plt.scatter(x=pos_x, y=pos_y)
plt.show()

