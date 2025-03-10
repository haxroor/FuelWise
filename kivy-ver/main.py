import json
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.behaviors import HoverBehavior #used in HoverlessMDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.chip import MDChip, MDChipText, MDChipLeadingIcon
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer, MDDialogContentContainer, \
    MDDialogSupportingText
from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemTrailingCheckbox
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem, MDSegmentButtonIcon, \
    MDSegmentButtonLabel
from kivymd.uix.selectioncontrol.selectioncontrol import MDSwitch
from kivymd.uix.slider import MDSlider, MDSliderHandle, MDSliderValueLabel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText, MDSnackbarButtonContainer, MDSnackbarActionButton, \
    MDSnackbarActionButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
#import matplotlib.pyplot as plt
from kivymd.utils.set_bars_colors import set_bars_colors
#from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd.uix.behaviors import HoverBehavior
from kivy.clock import Clock
from kivymd.theming import ThemeManager
from kivymd.dynamic_color import DynamicColor
from openai import OpenAI
'''from kivy.core.window import Window
Window.size = (1080/3, 2400/3)'''

#---global variables---
last_theme = None
last_palette = None
last_consumption_format = None
first_time = 1
global icon_color

#---defining the screens---

class FirstTimeScreen(MDScreen):
    pass
class MainScreen(MDScreen):
    pass
class SettingsScreen(MDScreen):
    pass

SCREENS = ["main_screen", "settings_screen", "first_time_screen"]

#-----------defining custom classes------------

class HoverlessMDCard(MDCard, HoverBehavior):
    def on_enter(self, *args):
        pass
    def on_leave(self, *args):
        pass
    def on_press(self, *args):
        pass

class HoverlessMDDialog(MDDialog, HoverBehavior):
    def on_enter(self, *args):
        pass
    def on_leave(self, *args):
        pass
    def on_press(self, *args):
        pass

class AdaptiveHeightMDBoxLayout(MDBoxLayout):
    def __init__(self, *children, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.adaptive_height = True
        for child in children:
            self.add_widget(child)

#-----------app------------

class FuelWiseApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__()
        self.theme_dialog = None
        self.palette_dialog = None
        self.consumption_format_dialog = None
        self.erase_data_dialog = None
        self.error_dialog = None
        self.entry_dialog = None
        self.liters_input = None
        self.odometer_input = None
        self.preferences = None
        self.data = None
        self.last_theme_data = None

    def load_data(self):
        with open('data.json', 'r') as f:
            try:
                self.data = json.load(f)
                if not self.data:
                    self.data = [{"km_tot": 0, "liters_tot": 0, "km_trip": 0, "liters_trip": 0, "consumption_trip": 0}]
            except (FileNotFoundError, json.JSONDecodeError):
                self.data = [{"km_tot": 0, "liters_tot": 0, "km_trip": 0, "liters_trip": 0, "consumption_trip": 0}]

    def load_preferences(self):
        try:
            with open('preferences.json', 'r') as f:
                self.preferences = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.preferences = {"last_theme": "Light", "last_palette": "Green", "last_consumption_format": "L/100km", "first_time": 1}
        return self.preferences

    def save_preferences(self, new_last_theme=None, new_last_palette=None, new_last_consumption_format=None):
        if new_last_theme is None:
            new_last_theme = last_theme
        if new_last_palette is None:
            new_last_palette = last_palette
        if new_last_consumption_format is None:
            new_last_consumption_format = last_consumption_format
        self.preferences['last_theme'] = new_last_theme
        self.preferences['last_palette'] = new_last_palette
        self.preferences['last_consumption_format'] = new_last_consumption_format
        self.preferences['first_time'] = 0
        with open('preferences.json', "w") as f:
            json.dump(self.preferences, f, indent=4)

    def on_start(self):
        global last_consumption_format
        global last_theme
        global first_time
        global last_palette
        preferences = self.load_preferences()
        last_consumption_format = preferences['last_consumption_format']
        last_theme = preferences['last_theme']
        first_time = preferences['first_time']
        last_palette = preferences['last_palette']
        if first_time:
            self.root.current = "first_time_screen"
        self.set_appearance()
        #self.populate_table() already called inside set_theme
        # ----settings buttons-----
        palette_setting = self.root.get_screen("settings_screen").ids.palette_setting
        palette_setting.bind(on_touch_down=lambda instance, touch: self.on_palette_setting_item_click(instance, touch))
        theme_setting = self.root.get_screen("settings_screen").ids.theme_setting
        theme_setting.bind(on_touch_down=lambda instance, touch: self.on_theme_setting_item_click(instance, touch))
        erase_data_setting = self.root.get_screen("settings_screen").ids.erase_data_setting
        erase_data_setting.bind(on_touch_down=lambda instance, touch: self.on_erase_data_setting_item_click(instance, touch))
        consumption_format_setting = self.root.get_screen("settings_screen").ids.consumption_format_setting
        consumption_format_setting.bind(on_touch_down=lambda instance, touch: self.on_consumption_format_setting_item_click(instance, touch))

    def on_palette_setting_item_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.open_palette_setting_dialog()

    def on_theme_setting_item_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.open_theme_setting_dialog()

    def on_erase_data_setting_item_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.open_erase_data_setting_dialog()

    def on_consumption_format_setting_item_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.open_consumption_format_setting_dialog()

    def exit_tutorial(self):
        global first_time
        first_time = 0
        self.root.current = "main_screen"
        self.save_preferences()

    #----------------theming----------------

    def set_bars_colors(self):
        set_bars_colors(
            self.theme_cls.primaryColor,  # status bar color
            self.theme_cls.primaryColor,  # navigation bar color
            "Light",  # icons color of status bar
        )

    def set_appearance(self, theme=None, palette=None):
        global last_theme
        global last_palette
        global icon_color
        global text_color
        # saving preferences before changing theme/palette
        theme = theme if theme is not None else last_theme
        last_theme = theme if theme is not None else last_theme
        palette = palette if palette is not None else last_palette
        last_palette = palette if palette is not None else last_palette
        self.save_preferences(new_last_theme=theme, new_last_palette=palette)
        # actual theme/palette change
        self.theme_cls.theme_style = theme
        self.theme_cls.primary_palette = palette
        icon_color = self.theme_cls.primaryColor
        text_color = self.theme_cls.onSecondaryContainerColor
        self.set_bars_colors()
        def update_background_color(*args):
            global icon_color
            # bg color
            color = list(self.theme_cls.secondaryContainerColor)
            color[3] = .21 if theme == "Dark" else .98
            color = tuple(color)
            def apply_background(sn, _):
                screen = self.root.get_screen(sn)
                if not hasattr(screen, 'background_rect'):
                    with screen.canvas.before:
                        screen.background_color = Color(*color)
                        screen.background_rect = Rectangle(size=screen.size, pos=screen.pos)
                screen.background_rect.pos = screen.pos
                screen.background_rect.size = screen.size
                screen.background_color.rgba = color
                def update_rect(instance, value):
                    screen.background_rect.size = screen.size
                    screen.background_rect.pos = screen.pos
                screen.bind(size=update_rect, pos=update_rect)
            for screen_name in SCREENS:
                Clock.schedule_once(lambda dt, sn=screen_name: apply_background(sn, dt), 0)
        Clock.schedule_once(update_background_color, 0.1)
        if self.palette_dialog:
            self.palette_dialog.dismiss()
        if self.theme_dialog:
            self.theme_dialog.dismiss()
        self.populate_table()

    def switch_theme(self):
        if last_theme == "Dark":
            self.set_appearance(theme="Light")
        else:
            self.set_appearance(theme="Dark")

    #----------------table,cards----------------

    def populate_table(self):
        main_scroll = self.root.get_screen('main_screen').ids.main_scroll
        main_scroll.clear_widgets()  # Clear existing widgets
        main_scroll.add_widget(MDLabel())
        main_scroll.add_widget(MDLabel())

        if len(self.data) == 1:
            no_entry_card = HoverlessMDCard(
                style="elevated",
                pos_hint={"center_x": .5},
                padding="16sp",
                size_hint=(None, None),
                size=(.5, "30sp"),
                orientation="vertical",
            )
            no_entry_card.add_widget(MDLabel(text="No data available. Please add two more entries.", halign='center'))
            main_scroll.add_widget(no_entry_card)
            return
        if len(self.data) == 2:
            one_entry_card = HoverlessMDCard(
                style="elevated",
                pos_hint={"center_x": .5},
                padding="16sp",
                size_hint=(None, None),
                size=(.5, "30sp"),
                orientation="vertical",
            )
            one_entry_card.add_widget(MDLabel(text="Only one entry available. Please add a new entry.", halign='center'))
            main_scroll.add_widget(one_entry_card)
            return

        #--------displaying cards--------

        total_km = (self.data[-1]['km_tot'])-(self.data[1]['km_tot'])
        total_liters = (self.data[-1]['liters_tot'])-(self.data[1]['liters_tot'])
        if last_consumption_format == "L/100km":
            total_consumption = total_liters*100/total_km
        else:
            total_consumption = total_km/total_liters

        '''color = list(self.theme_cls.primaryColor)
        color[3] = .15 if last_theme == "Dark" else .50'''
        #---average consumption icon card---
        avg_icon_card = HoverlessMDCard(
            style="elevated",
            pos_hint={"center_x": .5},
            size_hint = (.35, None),
            adaptive_height=True,
            padding="8sp",
            #theme_bg_color =  "Custom",
            #md_bg_color=color,
        )
        avg_icon_card.add_widget(MDLabel(
            text="Average Consumption",
            halign='center',
            font_style="Label",
            role="small",
            bold=True,
            size_hint_y = None,
            adaptive_height=True,
        ))
        main_scroll.add_widget(avg_icon_card)

        #---average consumption card---
        avg_card = HoverlessMDCard(
            style = "elevated",
            pos_hint = {"center_x": .5},
            size_hint = (.55, None),
            adaptive_height = True,
            #theme_bg_color="Custom",
            #md_bg_color=color,
        )
        avg_card.add_widget(
            MDBoxLayout(
                MDAnchorLayout(
                    MDLabel(text=" "),
                ),
                MDAnchorLayout(
                    MDBoxLayout(
                        MDAnchorLayout(
                            MDIcon(icon = "fuel", icon_color = icon_color,),
                            size_hint_x = None,
                            width = "24sp",
                        ),
                        MDAnchorLayout(
                            MDLabel(
                                text = f"{total_consumption:.2f}{last_consumption_format}",
                                font_style = "Title",
                                bold = True,
                                size_hint_x = None,
                                adaptive_width = True,
                                size_hint_y = None,
                                adaptive_height = True,
                            ),
                        ),
                        orientation = "horizontal",
                        size_hint_y = None,
                        adaptive_height = True,
                        size_hint_x = None,
                        width = "165sp",
                    ),
                    anchor_x="center",
                    anchor_y="center",
                ),
                MDLabel(
                    text=f"Last Entry: {self.data[-1]['km_tot']:.0f}km | {self.data[-1]['liters_tot']:.1f}L",
                    halign='center',
                    font_style="Label",
                    role="small",
                    text_color=text_color,
                    size_hint_y=None,
                    adaptive_height=True,
                ),
                spacing = "16sp",
                padding="6sp",
                orientation="vertical",
                size_hint_y=None,
                adaptive_height=True,
            )
        )
        main_scroll.add_widget(avg_card)

        #---trip icon card---
        trip_icon_card = HoverlessMDCard(
            style="elevated",
            pos_hint={"center_x": .5},
            size_hint = (.12, None),
            adaptive_height=True,
            padding="8sp",
            #theme_bg_color="Custom",
            #md_bg_color=color,
        )
        trip_icon_card.add_widget(MDLabel(
                text="Trips",
                halign='center',
                font_style="Label",
                role="small",
                bold=True,
                size_hint_y=None,
                adaptive_height=True,
        ))
        main_scroll.add_widget(trip_icon_card)

        #---trip card---
        trip_card = HoverlessMDCard(
            style = "elevated",
            pos_hint = {"center_x": .5},
            size_hint = (0.9, None),
            adaptive_height = True,
            padding="16sp",
            orientation = "vertical",
            #theme_bg_color="Custom",
            #md_bg_color=color,
        )
        #trip_card.add_widget(MDDivider())
        for i, item in enumerate(self.data):
            # --- Skipping the first two entries ---
            if i < 2:
                continue
            if last_consumption_format == "L/100km":
                consumption_trip = 100 / item['consumption_trip']
            else:
                consumption_trip = item['consumption_trip']

            row = MDBoxLayout(
                MDAnchorLayout(
                    MDIcon(icon = "trending-up", icon_color = icon_color,),
                    size_hint_x = None,
                    width = "24sp",
                ),
                MDAnchorLayout(
                    MDLabel(
                        text = f"  {consumption_trip:.2f}{last_consumption_format}",
                        size_hint_x = None,
                        adaptive_width = True,
                        size_hint_y = None,
                        adaptive_height = True,
                    ),
                    anchor_x="left",
                ),
                MDAnchorLayout(
                    MDLabel(
                        text = f"{item['liters_trip']:.1f}Lx{item['km_trip']:.0f}km",
                        font_style="Label",
                        role="small",
                        text_color= text_color,
                        size_hint_x = None,
                        adaptive_width = True,
                        size_hint_y = None,
                        adaptive_height = True,
                    ),
                    anchor_x = "right",
                ),
                orientation="horizontal",
                size_hint_y=None,
                height="30sp",
            )
            trip_card.add_widget(row)
            #trip_card.add_widget(MDDivider())

        main_scroll.add_widget(trip_card)

        main_scroll.add_widget(MDLabel())
        main_scroll.add_widget(MDLabel())

    #------------------------------------------------DIALOGS------------------------------------------------

    def open_entry_dialog(self):
        def save_entry():
            try:
                if not self.odometer_input.text or not self.liters_input.text:
                    return

                odometer = float(self.odometer_input.text)
                liters = float(self.liters_input.text)

                if odometer <= self.data[-1]['km_tot'] or liters <= self.data[-1]['liters_tot']:
                    MDSnackbar(
                        MDSnackbarSupportingText(
                            text="Invalid entry.",
                            font_style="Label",
                        ),
                        y="24sp",
                        pos_hint={"center_x": 0.5},
                        size_hint_y=None,
                        size_hint_x=0.6,
                        adaptive_height=True,
                        background_color=self.theme_cls.onPrimaryContainerColor,
                    ).open()
                    return

                if len(self.data) == 1:
                    new_entry = {
                        "km_tot": odometer,
                        "liters_tot": liters,
                        "km_trip": 0,
                        "liters_trip": 0,
                        "consumption_trip": 0,
                    }
                else:
                    new_entry = {
                        "km_tot": odometer,
                        "liters_tot": liters,
                        "km_trip": odometer - self.data[-1]['km_tot'],
                        "liters_trip": liters - self.data[-1]['liters_tot'],
                        "consumption_trip": (odometer - self.data[-1]['km_tot']) / (
                                    liters - self.data[-1]['liters_tot']),
                    }
                self.data.append(new_entry)
                with open("data.json", "w") as f:
                    json.dump(self.data, f, indent=4)
                self.populate_table()
                self.entry_dialog.dismiss()
                MDSnackbar(
                    MDSnackbarSupportingText(
                        text="Entry saved successfully.",
                    ),
                    y= "24sp",
                    orientation="horizontal",
                    pos_hint={"center_x": 0.5},
                    size_hint_x=0.5,
                    background_color=self.theme_cls.onPrimaryContainerColor,
                ).open()
            except ValueError:
                return

        self.odometer_input = MDTextField(
            MDTextFieldHintText(text="Odometer",
                                #font_style="Label"
                                ),
            mode="outlined",
            pos_hint={"center_y": 0.1},
        )

        self.liters_input = MDTextField(
            MDTextFieldHintText(text="Fuel",
                                #font_style="Label"
                                ),
            mode="outlined",
            pos_hint={"center_y": 0.1},
        )

        self.entry_dialog = HoverlessMDDialog(
            MDDialogHeadlineText(
                text="New Entry",
                halign="left",
            ),
            MDDialogSupportingText(
                text="Enter the mileage displayed on the odometer and the amount of fuel consumed since the last reset of the onboard computer.",
                halign="left",
            ),
            MDDialogContentContainer(
                MDBoxLayout(
                    MDBoxLayout( # prima sezione verticale
                        MDAnchorLayout(
                            MDIcon(icon="road", icon_color=icon_color),
                            size_hint_x=None,
                            width="24sp"
                        ),
                        MDAnchorLayout(  # odometer input
                            self.odometer_input,
                            size_hint_x=0.6,
                        ),
                        MDAnchorLayout(
                            MDIcon(icon="water", icon_color=icon_color),
                            size_hint_x=None,
                            width="24sp"
                        ),
                        MDAnchorLayout(  # liters input
                            self.liters_input,
                            size_hint_x=0.4,
                        ),
                        orientation="horizontal",
                        size_hint_y=None,
                        # adaptive_height=True,

                    ),
                    orientation="vertical",
                    size_hint_y=None,
                    adaptive_height=True,
                    pos_hint={"top": 1},
                    theme_bg_color="Custom",
                    #md_bg_color=(0, 1, 0, .5),
                ),
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Discard"),
                    style="text",
                    on_release=lambda x: self.entry_dialog.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="Apply"),
                    style="text",
                    on_release=lambda x: save_entry(),
                ),
                spacing="8sp",
            ),
            size_hint = (0.5, None)
        )
        self.entry_dialog.open()

    def open_palette_setting_dialog(self):
        self.palette_dialog = HoverlessMDDialog(
            MDDialogHeadlineText(
                text="Palette",
                halign="left",
            ),
            MDDialogSupportingText(
                text="Choose a color palette for the app.\n",
                halign="left",
            ),
            MDDialogContentContainer(
                MDBoxLayout(
                    MDBoxLayout(
                        MDListItem(
                            MDListItemHeadlineText(text="Red"),
                            on_release=lambda x: self.set_appearance(palette="Firebrick"),
                        ),
                        MDListItem(
                            MDListItemHeadlineText(text="Orange"),
                            on_release=lambda x: self.set_appearance(palette="Orange"),
                        ),
                        MDListItem(
                            MDListItemHeadlineText(text="Yellow"),
                            on_release=lambda x: self.set_appearance(palette="Gold"),
                        ),
                        MDListItem(
                            MDListItemHeadlineText(text="Green"),
                            on_release=lambda x: self.set_appearance(palette="Green"),
                        ),
                        MDListItem(
                            MDListItemHeadlineText(text="Blue"),
                            on_release=lambda x: self.set_appearance(palette="Aliceblue"),
                        ),
                        MDListItem(
                            MDListItemHeadlineText(text="Purple"),
                            on_release=lambda x: self.set_appearance(palette="Indigo"),
                        ),
                        spacing="8sp",
                        adaptive_height=True,
                        orientation="vertical",
                    ),
                    spacing="32sp",
                    adaptive_height=True,
                    orientation="vertical",
                ),
            ),
            size_hint=(0.5, None)
        )
        self.palette_dialog.open()

    def open_theme_setting_dialog(self):
        self.theme_dialog = HoverlessMDDialog(
            MDDialogHeadlineText(
                text="Theme",
                halign="left",
            ),
            MDDialogSupportingText(
                text="Choose a theme for the app.\n",
                halign="left",
            ),
            MDDialogContentContainer(),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Light"),
                    style="text",
                    #style="filled",
                    #theme_bg_color="Custom",
                    #md_bg_color=(1,1,1,1),
                    on_release=lambda x: self.set_appearance(theme="Light"),
                ),
                MDButton(
                    MDButtonText(text="Dark"),
                    style="text",
                    #style="filled",
                    #theme_bg_color="Custom",
                    #md_bg_color=(0,0,0,1),
                    on_release=lambda x: self.set_appearance(theme="Dark"),
                ),
                spacing = "8sp",
            ),
            size_hint=(0.5, None)
        )
        self.theme_dialog.open()

    def open_erase_data_setting_dialog(self):
        def erase_data():
            self.data = [{"km_tot": 0, "liters_tot": 0, "km_trip": 0, "liters_trip": 0, "consumption_trip": 0}]
            with open("data.json", "w") as f:
                json.dump(self.data, f, indent=4)
            self.populate_table()
            self.erase_data_dialog.dismiss()

        self.erase_data_dialog = HoverlessMDDialog(
            MDDialogHeadlineText(
                text="Erase Data",
                halign="left",
            ),
            MDDialogSupportingText(
                text="Are you sure you want to erase all data? This might be helpful to keep track of fuel consumptions after drastic changes (different driving style, tuning, on-board computer reset, etc...).\n",
                halign="left",
            ),
            MDDialogContentContainer(),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Discard"),
                    style="text",
                    on_release=lambda x: self.erase_data_dialog.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="Erase",),
                    style="filled",
                    theme_bg_color="Custom",
                    #md_bg_color=(243/255, 136/255, 141/255,1),
                    md_bg_color=(1, 0, 0, 1),
                    on_release=lambda x: erase_data()
                ),
                spacing="8sp",
            ),
            size_hint=(0.5, None)
        )
        self.erase_data_dialog.open()

    def open_consumption_format_setting_dialog(self):
        def consumption_format_switch(new_format):
            global last_consumption_format
            last_consumption_format = new_format
            self.save_preferences()
            self.populate_table()
            self.consumption_format_dialog.dismiss()

        self.consumption_format_dialog = HoverlessMDDialog(
            MDDialogHeadlineText(
                text="Consumption Format",
                halign="left",
            ),
            MDDialogSupportingText(
                text="Swith between L/100km and km/L.\n",
                halign="left",
            ),
            MDDialogContentContainer(),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="L/100km"),
                    style="text",
                    on_release=lambda x: consumption_format_switch("L/100km"),
                ),
                MDButton(
                    MDButtonText(text="km/L"),
                    style="text",
                    on_release=lambda x: consumption_format_switch("km/L")
                ),
            ),
            size_hint=(.5, None),
        )
        self.consumption_format_dialog.open()

    # ----------------------build------------------------
    def build(self):
        self.load_data()
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(SettingsScreen(name="settings_screen"))
        sm.add_widget(FirstTimeScreen(name="first_time_screen"))
        return sm

FuelWiseApp().run()
