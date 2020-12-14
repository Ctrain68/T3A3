from controllers.profiles_controller import profile
from controllers.user_controller import auth
from controllers.profile_images_controller import profile_images
from controllers.equipment_controller import equipment

registerable_controllers = [
    auth,
    profile,
    profile_images,
    equipment

]       