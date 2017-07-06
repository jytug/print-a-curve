from curve import create_mesh_from_parametrization
from sympy import N

variables = input("Type in the variables in the parametrisation, like: u v\n\t")

print("Type in the")
s1 = input("\tx coordinate of the parametrisation\n\t")
s2 = input("\ty coordinate of the parametrisation\n\t")
s3 = input("\tz coordinate of the parametrisation\n\t")

print("Type in the boundaries for the first variable")
umin = N((input("\tmin: ")))
umax = N((input("\tmax: ")))

print("Type in the boundaries for the second variable")
vmin = N((input("\tmin: ")))
vmax = N((input("\tmax: ")))

filename = input("Type in the file to be saved\n\t")

create_mesh_from_parametrization(variables, s1, s2, s3, None,
            umin, umax, vmin, vmax, filename=filename)
