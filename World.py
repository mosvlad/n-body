import numpy as np
import pygame
import random


class World:
    def __init__(self, width, height, depth):
        self.N = 10
        self.t = 0
        self.dt = 0.001
        self.softening = 0.1
        self.G = 1.0
        self.world_width = width
        self.world_height = height
        self.world_depth = depth

        np.random.seed(random.randint(0, 99999))

        self.mass = 5.0 * np.ones((self.N, 1))
        self.mass[0] = self.mass[1] * 5000
        self.pos = np.random.randn(self.N, 3)
        for i in range(len(self.pos)):
            self.pos[i][0] = random.randint(100, 400)
            self.pos[i][1] = random.randint(100, 400)
            self.pos[i][2] = random.randint(100, 400)

        self.vel = np.random.randn(self.N, 3)

        self.vel -= np.mean(self.mass * self.vel, 0) / np.mean(self.mass)

        self.acc = self.getAcc(self.pos, self.mass, self.G, self.softening)

        self.KE, self.PE = self.getEnergy(self.pos, self.vel, self.mass, self.G)

    def getAcc(self, pos, mass, G, softening):
        x = pos[:, 0:1]
        y = pos[:, 1:2]
        z = pos[:, 2:3]

        dx = x.T - x
        dy = y.T - y
        dz = z.T - z

        inv_r3 = (dx ** 2 + dy ** 2 + dz ** 2 + softening ** 2)
        inv_r3[inv_r3 > 0] = inv_r3[inv_r3 > 0] ** (-1.5)

        ax = G * (dx * inv_r3) @ mass
        ay = G * (dy * inv_r3) @ mass
        az = G * (dz * inv_r3) @ mass

        a = np.hstack((ax, ay, az))

        return a

    def getEnergy(self, pos, vel, mass, G):
        KE = 0.5 * np.sum(np.sum(mass * vel ** 2))

        x = pos[:, 0:1]
        y = pos[:, 1:2]
        z = pos[:, 2:3]

        dx = x.T - x
        dy = y.T - y
        dz = z.T - z

        inv_r = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        inv_r[inv_r > 0] = 1.0 / inv_r[inv_r > 0]

        PE = G * np.sum(np.sum(np.triu(-(mass * mass.T) * inv_r, 1)))

        return KE, PE

    def update(self):

        star_pos = self.pos[0]
        star_vel = self.vel[0]
        star_acc = self.acc[0]

        self.vel += self.acc * self.dt / 2.0

        self.pos += self.vel * self.dt

        self.acc = self.getAcc(self.pos, self.mass, self.G, self.softening)

        self.vel += self.acc * self.dt / 2.0

        self.t += self.dt

        self.pos[0] = star_pos
        self.vel[0] = star_vel
        self.acc[0] = star_acc

        for i in range(len(self.pos)):
            if self.pos[i][0] < 0: self.vel[i][0] = -self.vel[i][0]
            if self.pos[i][1] < 0: self.vel[i][1] = -self.vel[i][1]
            if self.pos[i][2] < 0: self.vel[i][2] = -self.vel[i][2]

            if self.pos[i][0] > self.world_width: self.vel[i][0] = -self.vel[i][0]
            if self.pos[i][1] > self.world_height: self.vel[i][1] = -self.vel[i][1]
            if self.pos[i][2] > self.world_depth: self.vel[i][2] = -self.vel[i][2]

    def draw(self, screen):
        for position in self.pos:
            color = int(position[2] / 3)
            #color = 255
            size = int(position[2] / 20)
            #size = 10
            if color < 0: color = 0
            if color > 255: color = 255
            pygame.draw.circle(screen, (color, color, color), (position[0], position[1]), size)
        pygame.draw.circle(screen, (255, 0, 0), (self.pos[0][0], self.pos[0][1]), int(self.pos[0][1] / 10))
