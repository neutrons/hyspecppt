#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:28:21 2024

@author: qmc
"""

import numpy as np
from scipy.constants import m_n, e, hbar
import matplotlib.pyplot as plt

SE2K = np.sqrt(2e-3*e*m_n) *1e-10/hbar

class Model:
    def __init__(self):
        pass

    def polarization_powder(self,Ei, EMin, S2, P, plot_options="alpha",left=True):
        #def Ei, Emin = - Ei to create Qmin, Qmax to generate plot range
        # Ei=20.0
        if EMin == None:
            EMin=-Ei 
        E = np.linspace(EMin, Ei*0.9, 200)
        
        kfmin = np.sqrt(Ei-EMin) * SE2K
        ki = np.sqrt(Ei) * SE2K
        
        # S2= 60
        #Create Qmin and Qmax
        Qmax = np.sqrt(ki**2 + kfmin**2 - 2*ki*kfmin*np.cos(np.radians(S2+30))) #Q=ki or Q=
        Qmin=0
        Q = np.linspace(Qmin, Qmax, 200)
        
        #Create 2D array
        E2d, Q2d = np.meshgrid(E, Q)
        
        Ef2d = Ei-E2d
        kf2d = np.sqrt(Ef2d) *SE2K
        
        Px=P[0]
        Pz=P[2]
        
        cos_theta = (ki**2 + kf2d**2 - Q2d**2)/ (2*ki*kf2d)
        cos_theta[cos_theta < np.cos(np.radians(S2+30))] = np.nan 
        cos_theta[cos_theta > np.cos(np.radians(S2-30))] = np.nan #cos(30)
        
        # cos_theta[cos_theta < -1] = np.nan
        # cos_theta[cos_theta > 1] = np.nan
        
        # theta=np.arccos(cos_theta)
        

        Qz = ki - kf2d*cos_theta
        Qx= (-1 if left else 1) * kf2d*np.sqrt((1-cos_theta**2))
        
        cos_ang_PQ = (Qx*Px + Qz*Pz)/Q2d/np.sqrt(Px**2+Pz**2)
        cos_ang_PQ[cos_ang_PQ**2 <0.4] = np.nan 
        cos_ang_PQ[cos_ang_PQ**2 >0.6] = np.nan
        ang_PQ = np.degrees(np.arccos(cos_ang_PQ))
        
        kf=np.sqrt(Ei-E)*SE2K
        
        Q_low = np.sqrt(ki**2 + kf**2 - 2*ki*kf*np.cos(np.radians(S2-30)))
        Q_hi = np.sqrt(ki**2 + kf**2 - 2*ki*kf*np.cos(np.radians(S2+30)))

        if plot_options == "alpha":
            return Q_low, Q_hi, E, Q2d, E2d, ang_PQ  
        
        if plot_options == "cos^2(a)":
            return Q_low, Q_hi, E, Q2d, E2d, np.cos(np.radians(ang_PQ))**2

        if plot_options == "cos^2(a)-sin^2(a)":
            return Q_low, Q_hi, E, Q2d, E2d, np.cos(np.radians(ang_PQ))**2 - np.sin(np.radians(ang_PQ))**2
        
        if plot_options == "(cos^2(a)+1)/2":
            return Q_low, Q_hi, E, Q2d, E2d, (np.cos(np.radians(ang_PQ))**2 +1)/2
        
        # if plot_options == "alpha":
        #     fig, ax = plt.subplots()
        #     pcm = ax.pcolormesh(Q2d, E2d, ang_PQ)
        #     ax.plot(Q_low, E)
        #     ax.plot(Q_hi, E)
            
        #     fig.colorbar(pcm, label= "Degrees")
        #     ax.set_xlabel(r"|Q| ($\AA^{-1}$)")
        #     ax.set_ylabel("E (meV)")
        #     fig.show()
            
        # if plot_options == "cos^2(a)":
        #     fig, ax = plt.subplots()
        #     pcm = ax.pcolormesh(Q2d, E2d, np.cos(np.radians(ang_PQ))**2)
        #     ax.plot(Q_low, E)
        #     ax.plot(Q_hi, E)
            
        #     fig.colorbar(pcm, label= r"$cos^2(\alpha)$")
        #     ax.set_xlabel(r"|Q| ($\AA^{-1}$)")
        #     ax.set_ylabel("E (meV)")
        #     fig.show()
            
        # if plot_options == "cos^2(a)-sin^2(a)":
        #     fig, ax = plt.subplots()
        #     pcm = ax.pcolormesh(Q2d, E2d, np.cos(np.radians(ang_PQ))**2 - np.sin(np.radians(ang_PQ))**2)
        #     ax.plot(Q_low, E)
        #     ax.plot(Q_hi, E)
            
        #     fig.colorbar(pcm, label= r"$cos^2(\alpha) - sin^2(\alpha)$")
        #     ax.set_xlabel(r"|Q| ($\AA^{-1}$)")
        #     ax.set_ylabel("E (meV)")
        #     fig.show()

        # if plot_options == "(cos^2(a)+1)/2":
        #     fig, ax = plt.subplots()
        #     pcm = ax.pcolormesh(Q2d, E2d, (np.cos(np.radians(ang_PQ))**2 +1)/2)
        #     ax.plot(Q_low, E)
        #     ax.plot(Q_hi, E)
            
        #     fig.colorbar(pcm, label= r"$\dfrac{cos^2(\alpha) - 1}{2}$")
        #     ax.set_xlabel(r"|Q| ($\AA^{-1}$)")
        #     ax.set_ylabel("E (meV)")
        #     fig.show()

if __name__ == "__main__":
    obj = Model()
    output = obj.polarization_powder(20, None, 60, [1,0,-1],plot_options="alpha",left=True)
    Q_low, Q_hi, E, Q2d, E2d, ang_PQ = output[0], output[1], output[2], output[3], output[4], output[5]
    
    fig, ax = plt.subplots()
    pcm = ax.pcolormesh(Q2d, E2d, ang_PQ)
    ax.plot(Q_low, E)
    ax.plot(Q_hi, E)
    
    fig.colorbar(pcm, label= "Degrees")
    ax.set_xlabel(r"|Q| ($\AA^{-1}$)")
    ax.set_ylabel("E (meV)")
    fig.show()

# fig.show()

#test case should be -95.6571
# Ef=30
# kf=np.sqrt(Ef)*SE2K
# Qx = -kf*np.sin(np.radians(30))
# Qz = ki-kf*np.cos(np.radians(30))

# print(np.degrees(np.arctan2(Qx,Qz)))