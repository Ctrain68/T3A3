from controllers.profiles_controller import profile
from controllers.user_controller import auth
from controllers.profile_images_controller import profile_images
from controllers.tribe_controller import tribe

registerable_controllers = [
    auth,
    profile,
    profile_images,
    tribe

]       