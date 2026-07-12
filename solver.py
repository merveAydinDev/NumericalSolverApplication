import numpy as np

def euler_method(f, x0, y0, h, n):
    x_vals = [x0]
    y_vals = [y0]
    for _ in range(n):
        y_next = y_vals[-1] + h * f(x_vals[-1], y_vals[-1])
        x_next = x_vals[-1] + h
        x_vals.append(x_next)
        y_vals.append(y_next)
    return x_vals, y_vals

def heun_method(f, x0, y0, h, n):
    x_vals = [x0]
    y_vals = [y0]
    for _ in range(n):
        x_n = x_vals[-1]
        y_n = y_vals[-1]
        
        # Kestirme adımı (Euler ile)
        y_predict = y_n + h * f(x_n, y_n)
        
        # Düzeltme adımı
        y_next = y_n + (h / 2) * (f(x_n, y_n) + f(x_n + h, y_predict))
        
        x_vals.append(x_n + h)
        y_vals.append(y_next)
    return x_vals, y_vals

def runge_kutta_4(f, x0, y0, h, n):
    # 4. Mertebeden Runge-Kutta yöntemi[cite: 639].
    x_vals = [x0]
    y_vals = [y0]
    for _ in range(n):
        x_n = x_vals[-1]
        y_n = y_vals[-1]
        
        k1 = f(x_n, y_n)
        k2 = f(x_n + h/2, y_n + h*k1/2)
        k3 = f(x_n + h/2, y_n + h*k2/2)
        k4 = f(x_n + h, y_n + h*k3)
        
        y_next = y_n + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
        x_vals.append(x_n + h)
        y_vals.append(y_next)
    return x_vals, y_vals

def adams_bashforth_moulton(f, x0, y0, h, n):
    # Adams Kestirme-Düzeltme yöntemi[cite: 709].
    if n < 4:
        return runge_kutta_4(f, x0, y0, h, n)
        
    # İlk 4 noktayı RK4 ile buluyoruz
    x_vals, y_vals = runge_kutta_4(f, x0, y0, h, 3)
    
    for i in range(3, n):
        x_i = x_vals[-1]
        
        f_i = f(x_vals[i], y_vals[i])
        f_i1 = f(x_vals[i-1], y_vals[i-1])
        f_i2 = f(x_vals[i-2], y_vals[i-2])
        f_i3 = f(x_vals[i-3], y_vals[i-3])
        
        # Kestirme (Predictor) Formülü [cite: 703]
        y_predict = y_vals[i] + (h / 24) * (55*f_i - 59*f_i1 + 37*f_i2 - 9*f_i3)
        x_next = x_i + h
        
        # Düzeltme (Corrector) Formülü [cite: 707]
        f_next = f(x_next, y_predict)
        y_correct = y_vals[i] + (h / 24) * (9*f_next + 19*f_i - 5*f_i1 + f_i2)
        
        x_vals.append(x_next)
        y_vals.append(y_correct)
    return x_vals, y_vals

def milne_simpson(f, x0, y0, h, n):
    # Milne-Simpson yöntemi[cite: 505].
    if n < 4:
        return runge_kutta_4(f, x0, y0, h, n)
        
    x_vals, y_vals = runge_kutta_4(f, x0, y0, h, 3)
    
    for i in range(3, n):
        x_i = x_vals[-1]
        
        f_i = f(x_vals[i], y_vals[i])
        f_i1 = f(x_vals[i-1], y_vals[i-1])
        f_i2 = f(x_vals[i-2], y_vals[i-2])
        
        # Kestirme (Milne) Formülü [cite: 589]
        y_predict = y_vals[i-3] + (4*h / 3) * (2*f_i2 - f_i1 + 2*f_i)
        x_next = x_i + h
        
        # Düzeltme (Simpson) Formülü [cite: 589]
        f_next = f(x_next, y_predict)
        y_correct = y_vals[i-1] + (h / 3) * (f_next + 4*f_i + f_i1)
        
        x_vals.append(x_next)
        y_vals.append(y_correct)
    return x_vals, y_vals