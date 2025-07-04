import bpy, os
from .config import *


class BL_KEY_Pan_Preferences(bpy.types.AddonPreferences):
    bl_idname = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

    key_pan_up: bpy.props.StringProperty(
        name="Pan Up Key",
        description="Key to pan the view up (e.g., 'NumpadUp', 'W', 'Space', 'LButton').",
        default="NumpadUp",
    )
    key_pan_down: bpy.props.StringProperty(
        name="Pan Down Key",
        description="Key to pan the view down (e.g., 'NumpadDown', 'S').",
        default="NumpadDown",
    )
    key_pan_left: bpy.props.StringProperty(
        name="Pan Left Key",
        description="Key to pan the view left (e.g., 'NumpadLeft', 'A').",
        default="NumpadLeft",
    )
    key_pan_right: bpy.props.StringProperty(
        name="Pan Right Key",
        description="Key to pan the view right (e.g., 'NumpadRight', 'D').",
        default="NumpadRight",
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Customize Panning Hotkeys (Windows Only)", icon='FILE')
        
        # Define a helper method for layout
        def draw_key_setting(box, prop_name, label, context_self):
            row = box.row(align=True)
            row.prop(context_self, prop_name)
            row.scale_x = 0.3
            op = row.operator("key.set_key_modal", text="Set Key")
            op.target_property = prop_name
            op.target_label = label
        
        # Call the helper function for each key
        draw_key_setting(box, "key_pan_up", "Pan Up Key", self)
        draw_key_setting(box, "key_pan_down", "Pan Down Key", self)
        draw_key_setting(box, "key_pan_left", "Pan Left Key", self)
        draw_key_setting(box, "key_pan_right", "Pan Right Key", self)


        row = box.row(align=False)
        row.operator("key.generate_and_recompile_script", 
                     text="🛠️                     Recompile                       ")
        row.operator("key.reset_keys", 
                     text="🔄️                     Reset Keys                    ")

        box.separator()
        box.label(text="Important Notes:")
        row_template = box.row(align=False)
        row_template.label(text="- Other settings (speed, acceleration) can be edited in:")
        row_template.scale_x = 0.5
        row_template.operator("key.open_template_file", text='TEMPLATE FILE', icon='FILE_SCRIPT')
        box.label(text="- The template script is an AHK scrip. After editing The template, click Rcompile or Reset Keys.")
        box.label(text="- Either will do as per your changes.")
