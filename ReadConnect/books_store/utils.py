import os

module_dir = os.path.dirname(__file__)
parent_directory = os.path.dirname(module_dir)


def add_filter(filters, field_name, value, operator=None):
    if value:
        if operator:
            filters[f"{field_name}__{operator}"] = value
        else:
            filters[field_name] = value



def profile_image_path(instance, filename):
    return f'profile_images/{instance.user.username}.png'