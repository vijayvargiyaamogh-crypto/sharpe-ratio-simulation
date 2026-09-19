from random import gauss
from math import log, exp
import matplotlib.pyplot as plt

def testSharpe(): 
    """This is the author's rough work and isn't part of the simulation."""

    P_init = float(input("Enter initial sum (principal): "))
    period = float(input("Enter time period (years): "))
    r_f = float(input("Enter annual risk-free rate (%): "))/100

    n = round(period * 252) # no. of trading days
    P = [P_init for i in range(n+1)]
    r = [(P[i+1]-P[i])/P[i] for i in range(n)] # r[i] = return on day i+1
    R_p = sum(r)/n # average daily return
    Sigma = (sum((r[i]-R_p)**2 for i in range(n))/(n-1))**0.5 # daily volatility
    R_f = (1 + r_f)**(1/252) - 1 # daily risk-free return

    SR = (R_p - R_f)/Sigma * (252**0.5) # Sharpe ratio (annualized)
    print(f"SR = {SR}")

def SharpeRatio(r_p, r_f, n, Lambda, z):
    # Lambda controls the magnitude of fluctuations in the log-returns

    x = [log(1 + r_p)/252 + Lambda*z[i] for i in range(n)] # log-return on day i+1
    r = [exp(x[i])-1 for i in range(n)] # r[i] = return on day i+1
    R_p = sum(r)/n # average daily return
    Sigma = (sum((r[i]-R_p)**2 for i in range(n))/(n-1))**0.5 # daily volatility
    R_f = (1 + r_f)**(1/252) - 1 # daily risk-free return
    SR_test = (R_p - R_f)/Sigma * (252**0.5) # Sharpe ratio for given Lambda
    return SR_test

def simulate():
    P_init = float(input("Enter initial sum (principal): "))
    period = float(input("Enter time period (years): "))
    r_p = float(input("Enter annual return (%): "))/100
    r_f = float(input("Enter annual risk-free rate (%): "))/100
    SR = float(input("Enter Sharpe ratio: ")) # annualized

    n = round(period * 252) # no. of trading days
    z = [gauss(0, 1) for i in range(n)] # n Gaussian random variables

    z_mean = sum(z)/n
    z = [z[i]-z_mean for i in range(n)] # centering (mean = 0)

    z_std = (sum(z[i]**2 for i in range(n))/(n-1))**0.5
    z = [z[i]/z_std for i in range(n)] # standardization (std = 1)

    R_p = (1 + r_p)**(1/252) - 1 # daily return corresponding to annual return r_p
    R_f = (1 + r_f)**(1/252) - 1 # daily risk-free return
    Lambda_est = (R_p - R_f)*(252**0.5)/((1 + R_p)*SR) # approximate Lambda

    Lambda_low = Lambda_est
    SR_low = SharpeRatio(r_p, r_f, n, Lambda_low, z)

    Lambda_high = Lambda_est
    SR_high = SharpeRatio(r_p, r_f, n, Lambda_high, z)

    # Determining interval for Lambda
    while SR_low < SR:
        Lambda_low /= 2
        SR_low = SharpeRatio(r_p, r_f, n, Lambda_low, z)
    while SR_high > SR:
        Lambda_high *= 2 
        SR_high = SharpeRatio(r_p, r_f, n, Lambda_high, z)

    # Bisection search inside interval
    Lambda = (Lambda_low + Lambda_high)/2
    SR_test = SharpeRatio(r_p, r_f, n, Lambda, z)

    while abs(SR_test - SR) > 1e-6:
        if SR_test > SR:
            Lambda_low = Lambda
        else:
            Lambda_high = Lambda

        Lambda = (Lambda_low + Lambda_high)/2
        SR_test = SharpeRatio(r_p, r_f, n, Lambda, z)

    x = [log(1 + r_p)/252 + Lambda*z[i] for i in range(n)] # log-return on day i+1
    r = [exp(x[i])-1 for i in range(n)] # r[i] = return on day i+1

    P = [P_init]
    for i in range(n):
        P.append(P[i]*(1+r[i]))

    print("\nSimulation details:")
    print(f"Lambda = {Lambda}")
    print(f"Sharpe ratio = {SR_test}")
    print(f"Sum after {period} years = {P[n]}")

    plt.plot(range(n+1), P)
    plt.xlabel("Trading day")
    plt.ylabel("Principal")
    plt.show()

simulate()