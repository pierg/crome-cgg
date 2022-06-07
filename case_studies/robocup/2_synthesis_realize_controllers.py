from tools.persistence import Persistence
from robocup import output_folder_name

"""Load CGG"""
cgg = Persistence.load_cgg(output_folder_name)

"""Realize Specification and Transition Controllers indicating the Maximum Transition Time"""
cgg.realize_all(t_trans=3)
print(cgg)

"""Save CGG again with the controllers information"""
cgg.save()

"""Save CGG for persistence"""
Persistence.dump_cgg(cgg)
