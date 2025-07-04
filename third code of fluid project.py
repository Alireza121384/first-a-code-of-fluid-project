#result
import csv
import os
import sys
from typing import List , Tuple , Optional
def read_csv_cols (frame: str , col_q: int , col_h: int) -> Tuple[List[\
    float] , List[float]]:
    try:
        with open (fname , newline='' , encoding='utf.8') as f:
            rdr=csv.reader(f)
            for row in rdr:
                try:
                    q=float(row[col_q])
                    h=float(row[col_h])
                except (IndexError , ValueError):
                    continue
                Q.append(q)
                H.append(h)
    except FileNotFoundError:
        return [] , []
    return Q , H
def point_in_poly(x: float, y: float, poly_x: List\
                  [float], poly_y: List[float]) -> bool:
    n, inside = len(poly_x), False
    j = n - 1
    for i in range(n):
        xi, yi = poly_x[i], poly_y[i]
        xj, yj = poly_x[j], poly_y[j]
        if ((yi > y) != (yj > y)) and \
           (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            inside = not inside
        j = i
    return inside
def linear_interp(x0: float, x1: float, y0: float\
                  , y1: float, x: float) -> float:
    if x1 == x0:
        return (y0 + y1) / 2.0
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
def interp_1d(x_list: List[float], y_list: List[float], x: float\
              ) -> Optional[float]:
    if len(x_list) < 2:
        return None
    for k in range(len(x_list) - 1):
        if x_list[k] <= x <= x_list[k + 1]:
            return linear_interp(x_list[k], x_list[k + 1],
                                 y_list[k], y_list[k + 1], x)
    return None
#properties
i_list = [32, 40, 50, 65, 80, 100, 125]
j_list = [125, 160, 200, 250]
pump_curves = {}          # (i,j) → (Q[], H[])
for i_val in i_list:
    for j_val in j_list:
        fname = f'{i_val}-{j_val}.csv'
        Q, H = read_csv_cols(fname, 1, 2)
        if Q:
            pump_curves[(i_val, j_val)] = (Q, H)
try:
    Q_user = float(input('» Required Q (m³/h): '))
    H_user = float(input('» Required h_pump (m): '))
except ValueError:
    sys.exit('invalid input')
#pump family
found_family: Optional[Tuple[int, int]] = None
for (i_val, j_val), (Q, H) in pump_curves.items():
    if point_in_poly(Q_user, H_user, Q, H):
        found_family = (i_val, j_val)
        break
if not found_family:
    sys.exit('No pump family covers this duty point.')
i_val, j_val = found_family
print(f'️  proper family: {i_val}-{j_val}')
#Impeller diameter
d_file = f'd-{i_val}-{j_val}.csv'
d_list_raw, _ = read_csv_cols(d_file, 0, 0)
d_list = [d for d in d_list_raw if d > 0]
if not d_list:
    sys.exit(f'Impeller diameter file («{d_file}») unavailable')
hq_pairs = []
for d in d_list:
    fname =(f'{i_val}-{j_val}-{int(d)}.csv')
    Q_d, H_d = read_csv_cols(fname, 1, 2)
    pairs = sorted((q, h) for q, h in zip(Q_d, H_d))
    if not pairs:
        continue
    Q_sorted, H_sorted = zip(*pairs)
    H_at_Q = interp_1d(list(Q_sorted), list(H_sorted), Q_user)
    if H_at_Q is not None:
        hq_pairs.append((H_at_Q, d))
if len(hq_pairs)<2:
    sys.exit('Data is not match with Impeller diameter')
hq_pairs.sort()
H_values, D_values = zip(*hq_pairs)
D_interp = interp_1d(list(H_values), list(D_values), H_user)
if D_interp is None:
    sys.exit('  h_pump is not match with Impeller diameter.')
print(f' Impeller diameter={D_interp:.2f}mm')
P_interp_pairs=[]
for d in d_list:
    fname = f'{i_val}-{j_val}---{int(d)}.csv'
    Q_d, P_d = read_csv_cols(fname, 1, 2)
    pairs = sorted((q, p) for q, p in zip(Q_d, P_d))
    if not pairs:
        continue
    Q_sorted, P_sorted = zip(*pairs)
    P_at_Q = interp_1d(list(Q_sorted), list(P_sorted), Q_user)
    if P_at_Q is not None:
        P_interp_pairs.append((d, P_at_Q))
if len(P_interp_pairs) < 2:
    print('P is invalid.')
    P_user = None
else:
    P_interp_pairs.sort()
    D_vals, P_vals = zip(*P_interp_pairs)
    P_user = interp_1d(list(D_vals), list(P_vals), D_interp)
    if P_user is None:
        print('  P is not match with Impeller diameter.')
    else:
        print(f' P_shaft={P_user:.3f} KW')
#efficiency
eta_file = f'e-{i_val}-{j_val}.csv'
eta_list_raw, _ = read_csv_cols(eta_file, 0, 0)
eta_levels = [e for e in eta_list_raw if e > 0]
best_eta = None
best_eta_diff = 1e9
for eta in eta_levels:
    fname = f'{i_val}-{j_val}--{int(eta)}.csv'
    Q_e, H_e = read_csv_cols(fname, 1, 2)
    pairs = sorted((q, h) for q, h in zip(Q_e, H_e))
    if not pairs:
        continue
    Q_sorted, H_sorted = zip(*pairs)
    H_at_Q = interp_1d(list(Q_sorted), list(H_sorted), Q_user)
    if H_at_Q is None:
        continue
    diff = abs(H_at_Q - H_user)
    if diff < best_eta_diff:
        best_eta_diff = diff
        best_eta=eta
if best_eta is None:
    print('eta is not match with other data')
else:
    print(f' eta={best_eta:.2f} %')
print('\n------------summary------------')
print(f'pump:        {i_val}-{j_val}')
print(f'Q (m³/h):   {Q_user}')
print(f'h_pump (m):      {H_user}')
print(f'D (mm):     {D_interp:.2f}')
if P_user is not None:
    print(f'P_shaft (kW):     {P_user:.3f}')
if best_eta is not None:
    print(f'eta  (%):     {best_eta:.2f}')
