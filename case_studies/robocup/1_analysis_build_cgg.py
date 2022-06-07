from core.cgg import Node
from core.cgg.exceptions import CGGException
from robocup import output_folder_name
from tools.persistence import Persistence

try:

    """Load the goals"""
    set_of_goals = Persistence.load_goals(output_folder_name)

    """Automatically build the CGG"""
    cgg = Node.build_cgg(set_of_goals)
    print(cgg)

    """Setting the saving folder"""
    cgg.set_session_name(output_folder_name)
    """Save CGG as text file"""
    cgg.save()
    """Save CGG so that it can be loaded later"""
    Persistence.dump_cgg(cgg)


except CGGException as e:
    raise e
