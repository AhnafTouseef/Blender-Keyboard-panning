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
        
        # UI for Pan Up Key
        row = box.row(align=True)
        row.prop(self, "key_pan_up")
        row.scale_x = 0.3
        op = row.operator("key.set_key_modal", text="Set Key")
        op.target_property = "key_pan_up"
        op.target_label = "Pan Up Key" # Pass label for better modal feedback

        # UI for Pan Down Key
        row = box.row(align=True)
        row.prop(self, "key_pan_down")
        row.scale_x = 0.3
        op = row.operator("key.set_key_modal", text="Set Key")
        op.target_property = "key_pan_down"
        op.target_label = "Pan Down Key"

        # UI for Pan Left Key
        row = box.row(align=True)
        row.prop(self, "key_pan_left")
        row.scale_x = 0.3
        op = row.operator("key.set_key_modal", text="Set Key")
        op.target_property = "key_pan_left"
        op.target_label = "Pan Left Key"

        # UI for Pan Right Key
        row = box.row(align=True)
        row.prop(self, "key_pan_right")
        row.scale_x = 0.3
        op = row.operator("key.set_key_modal", text="Set Key")
        op.target_property = "key_pan_right"
        op.target_label = "Pan Right Key"

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

        # box.label(text="- The generated script will be '%s' and compiled to '%s'." % (GENERATED_FILENAME, COMPILED_FILENAME))

