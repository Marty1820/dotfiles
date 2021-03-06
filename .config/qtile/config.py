# ███╗░░░███╗░█████╗░██████╗░████████╗██╗░░░██╗
# ████╗░████║██╔══██╗██╔══██╗╚══██╔══╝╚██╗░██╔╝
# ██╔████╔██║███████║██████╔╝░░░██║░░░░╚████╔╝░
# ██║╚██╔╝██║██╔══██║██╔══██╗░░░██║░░░░░╚██╔╝░░
# ██║░╚═╝░██║██║░░██║██║░░██║░░░██║░░░░░░██║░░░
# ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░

# IMPORTS
from imp import create_dynamic
import os
import re
import subprocess
from typing import List  # noqa: F401
from libqtile import qtile, bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile.utils import guess_terminal
from libqtile.widget.battery import Battery, BatteryState
from libqtile.widget.volume import Volume

#Dracula color theme
theme = {"background": "#282a36",
        "current": "#44475a",
        "selection": "#44475a",
        "foreground": "#f8f8f2",
        "comment": "#6272a4",
        "cyan": "#8be9fd",
        "green": "#50fa7b",
        "orange": "#ffb86c",
        "pink": "#ff79c6",
        "purple": "#bd93f9",
        "red": "#ff5555",
        "yellow": "#f1fa8c"}

#Variables/Programs
mod = "mod4"                        # Sets mod key to SUPER
home = os.path.expanduser('~')      # Allow using 'home +' to expand ~
myTerm = "alacritty"                # Default Terminal application
myBrowser = "brave"                 # Web browser
myFilemgr = "nemo"                  # File Manager
myEditor = "gedit"                  # Text editor
myAppLauncher = "rofi -show drun -theme '~/.config/rofi/config.rasi'"

# Keybindings
keys = [
  ### Essentials/launching apps
  Key([mod], "Return",
    lazy.spawn(myTerm),
    desc="Launches My Terminal"
    ),
  Key([mod], "b",
    lazy.spawn(myBrowser),
    desc="Launches My Web Browser"
    ),
  Key([mod], "e",
    lazy.spawn(myFilemgr),
    desc="Launches My File Manager"
    ),
  Key([mod], "a",
    lazy.spawn(myEditor),
    desc="Launches Text Editor"
    ),
  Key([mod], "Escape",
    lazy.spawn([home + '/.config/rofi/scripts/powermenu.sh'])
    ),
  Key([mod, "shift"], "c",
    lazy.window.kill(),
    desc="Kill focused window"
    ),
  Key([mod], "d",
    lazy.spawn(myAppLauncher),
    desc="Application Launcher"
    ),
  Key([mod], "r",
    lazy.spawncmd(),
    desc="Spawn a command using a prompt widget"
    ),
  # Qtile/layout commands
  Key([mod], "space",
    lazy.next_layout(),
    desc="Toggle between layouts"
    ),
  Key([mod, "shift"], "r",
    lazy.restart(),
    desc="Restart Qtile"
    ),
  # Moving windows.
  Key([mod, "shift"], "h",
    lazy.layout.shuffle_left(),
    desc="Move window to the left"
    ),
  Key([mod, "shift"], "l",
    lazy.layout.shuffle_right(),
    desc="Move window to the right"
    ),
  Key([mod, "shift"], "j",
    lazy.layout.shuffle_up(),
    desc="Move window up"
    ),
  Key([mod, "shift"], "k",
    lazy.layout.shuffle_down(),
    desc="Move window down"
    ),
  # Window changing commands
  Key([mod, "control"], "h",
    lazy.layout.shrink(),
    desc="Shrink window"
    ),
  Key([mod, "control"], "l",
    lazy.layout.grow(),
    desc="Grow window"
    ),
  Key([mod], "n",
    lazy.layout.normalize(),
    desc="Reset all window sizes"
    ),
  Key([mod], "m",
    lazy.layout.maximize(),
    desc='toggle window between minimum and maximum sizes'
    ),
  Key([mod], "f",
    lazy.window.toggle_fullscreen(),
    desc='toggle fullscreen'
    ),
  ## Function keys
  # Screen Brightness
  Key([], 'XF86MonBrightnessUp',
    #lazy.spawn('xbacklight -inc 10')
    lazy.spawn(home + '/.config/dunst/scripts/backlight.sh up')
    ),
  Key([], 'XF86MonBrightnessDown',
    #lazy.spawn('xbacklight -dec 10')
    lazy.spawn(home + '/.config/dunst/scripts/backlight.sh down')
    ),
  # Audio/Volume
  Key([], 'XF86AudioMute',
    #lazy.spawn('amixer -q set Master toggle')
    lazy.spawn(home + '/.config/dunst/scripts/volume.sh mute')
    ),
  Key([], 'XF86AudioRaiseVolume',
    #lazy.spawn('amixer -q set Master 1%+ unmute')
    lazy.spawn(home + '/.config/dunst/scripts/volume.sh up')
    ),
  Key([], 'XF86AudioLowerVolume',
    #lazy.spawn('amixer -q set Master 1%- unmute')
    lazy.spawn(home + '/.config/dunst/scripts/volume.sh down')
    ),
  Key([mod], 'XF86AudioRaiseVolume',
    lazy.spawn('amixer -q set Master 10%+ unmute')
    ),
  Key([mod], 'XF86AudioLowerVolume',
    lazy.spawn('amixer -q set Master 10%- unmute')
    ),
  #Screenshots
  Key([], 'Print',
    lazy.spawn("scrot -e 'mv $f ~/Pictures/Screenshot 2>/dev/null'")
    ),
  Key(["mod1"], 'Print',
    lazy.spawn("scrot -u -e 'mv $f ~/Pictures/Screenshot 2>/dev/null'"))
]
### WIDGET REPLACEMENTS ###
# Battery Icon & % | Replaces widget.Battery
class MyBattery(Battery):
  def build_string(self, status):
    symbols = ""
    index = int(status.percent * 10)
    index = max(index, 0) # 0 or higher
    index = min(index, 9) # 9 or lower start at 0
    char = symbols[index]
    if status.state == BatteryState.CHARGING:
      char += ""
      if status.state == BatteryState.UNKNOWN:
        char = ""
    return self.format.format(char=char, percent=status.percent)

battery = MyBattery(
  format = '{char} {percent:2.0%}',
    foreground = theme["cyan"],
    notify_below = 10,
)

# Audio Volume/still needs work | replacing widget.Volume
class MyVolume(Volume):
  def create_amixer_command(self, *args):
    return super().create_amixer_command("-M")
  def _update_drawer(self):
    if self.volume <= 0:
      self.volume = '0%'
      self.text = '🔇' + str(self.volume)
    elif self.volume < 30:
      self.text = '🔈' + str(self.volume) + '%'
    elif self.volume < 80:
      self.text = '🔉' + str(self.volume) + '%'
    else: # self.volume >=80:
      self.text = '🔊' + str(self.volume) + '%'

    def restore(self):
      self.timer_setup()

volume = MyVolume(
  foreground = theme["purple"],
)

# WiFi icon used in widget.GenPollText | sets icon for widget.Net
def network_con():
  wifi = "wlan0"
  eth = "eth0"
  vpn = "wg0"
  icon = ''
  command = "ip a | egrep 'wlan0|eth0|wg0' | grep 'inet'"
  proc = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE)
  output = proc.stdout.read()
  words = output.split()
  if vpn in words:
    icon = '旅'
  if eth in words:
    icon = icon + '歷'
  if wifi in words:
    icon = icon + ''
  if icon == '':
    icon = ''
  return icon

# Remove portions of windows name
def parse_func(text):
  for string in [" - Brave", " - gedit", " - Visual Studio Code"]:
    text = text.replace(string, "")
  return text

# Groups using Names istead of numbers
# See https://docs.qtile.org/en/stable/manual/config/groups.html
groups = [Group(""),
          Group("爵"),
          Group(""),
          Group(""),
          Group(""),
          Group("碌", layout='treetab'),
          Group("", layout='floating')]
# allow [S]mod4+1 through [S]mod4+0 to bind to groups; if you bind your groups by hand in your config, you don't need to do this.
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

#Used layouts
layouts = [
  layout.MonadTall(
    border_width = 2,
    border_focus = theme["purple"],
    border_normal = theme["background"],
    margin = 4,
    ),
  layout.Max(),
  layout.Floating(
    border_width = 2,
    border_focus = theme["purple"],
    border_normal = theme["background"],
    ),
  layout.TreeTab(
    font = "Hack",
    fontsize = 20,
    border_width = 2,
    sections = [''],
    bg_color = theme["background"],
    active_bg = theme["current"],
    active_fg = theme["purple"],
    inactive_bg = theme["background"],
    inactive_fg = theme["foreground"],
    urgent_bg = theme["background"],
    urgent_fg = theme["red"],
    panel_width = 185,
    ),
]

# Widget default settings
widget_defaults = dict(
  font = 'mononoki Nerd Font Mono',
  fontsize = 20,
  padding = 2,
  background = theme["background"],
)
extension_defaults = widget_defaults.copy()

#Setup bar
screens = [
  Screen(
    top=bar.Bar(
      [
      widget.CurrentLayoutIcon(
        custom_icon_paths = [(home + "/.config/qtile/icons")],
        foreground = theme["foreground"],
        scale = 0.8,
        ),
      widget.GroupBox(
        active = theme["green"],
        background = theme["background"],
        block_highlight_text_color = theme["purple"],
        disable_drag = True,
        foreground = theme["foreground"],
        fontsize = 32,
        highlight_color = theme["selection"],
        highlight_method = "line",
        inactive = theme["foreground"],
        urgent_border = theme["red"],
        ),
      widget.Prompt(
        prompt = 'Run: ',
        padding = 5,
        foreground = theme["purple"],
        bell_style = 'visual',
        visual_bell_color = theme["red"],
        ignore_dups_history = True,
        ),
      widget.WindowName(
        format = '{name}',
        empty_group_string = "Software is like sex; it's better when it's free. - Linux Torvald 1996",
        foreground = theme["foreground"],
        parse_text = parse_func,
        ),
      widget.CheckUpdates(
        update_interval = 300,
        distro = "Arch_checkupdates",
        display_format = " {updates} pkgs",
        no_update_string = "",
        mouse_callbacks = {'Button1': lazy.spawn(myTerm + ' -e paru -Syu')},
        foreground = theme["red"],
        colour_no_updates = theme["background"],
        colour_have_updates = theme["red"],
        ),
      widget.Sep(
        foreground = theme["foreground"],
        ),
       widget.Systray(
        icon_size = 22,
        foreground = theme["comment"],
        ),
      widget.Sep(
        foreground = theme["foreground"],
        ),
      widget.GenPollText(
        func = network_con,
        foreground = theme["green"],
        update_interval = 5,
        ),
      widget.Net(
        format = '{total}',
        foreground = theme["green"],
        mouse_callbacks = {'Button1': lazy.spawn('nm-connection-editor')},
        ),
      widget.Sep(
        foreground = theme["foreground"],
        ),
      widget.TextBox(
        foreground = theme["orange"],
        text = 'CPU ',
        ),
      widget.CPU(
        foreground = theme["orange"],
        fmt = '{}',
        format = '💻{load_percent} ',
        ),
      widget.ThermalSensor(
        threshold = 70,
        foreground_alert = theme["red"],
        foreground = theme["orange"],
        fmt = '{}',
        ),
      widget.Sep(
        foreground = theme["foreground"],
        ),
      widget.TextBox(
        foreground = theme["pink"],
        text = 'MEM ',
        ),
      widget.Memory(
        mouse_callbacks = {'Button1': lazy.spawn(myTerm + ' -e btop')},
        foreground = theme["pink"],
        fmt = '{}',
        measure_mem = 'G',
        format = '{MemUsed:.1f}{mm}/{MemTotal:.0f}{mm}',
        update_interval = '1',
        ),
      widget.DF(
        foreground = theme["pink"],
        warn_color = theme["red"],
        format = ' {r:.0f}',
        partition = '/',
        visible_on_warn = False,
        ),
      widget.Sep(
        foreground = theme["foreground"],
        ),
      volume,
      widget.Sep(
        foreground = theme["foreground"],
        ),
      widget.Clock(
        format = ' %b %d %I:%M%p',
        foreground = theme["yellow"],
        mouse_callbacks = {'Button1': lazy.spawn(myBrowser + ' https://calendar.google.com')},
        ),
      widget.Sep(
        foreground = theme["foreground"],
        ),
      battery,
      ],
      24,
    ),
  ),
]

# Allows dragging floating layouts.
mouse = [
  Drag([mod], "Button1", lazy.window.set_position_floating(),
    start=lazy.window.get_position()),
  Drag([mod], "Button3", lazy.window.set_size_floating(),
    start=lazy.window.get_size()),
  Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False

# Set floating for certain apps
floating_layout = layout.Floating(float_rules=[
  # Run the utility of `xprop` to see the wm class and name of an X client.
  *layout.Floating.default_float_rules,
  Match(wm_class='confirm'),
  Match(wm_class='dialog'),
  Match(wm_class='download'),
  Match(wm_class='error'),
  Match(wm_class='file_progress'),
  Match(wm_class='notification'),
  Match(wm_class='nm-connection-editor'),
  Match(wm_class='xfce4-power-manager-settings'),
  Match(wm_class='bitwarden'),
  Match(wm_class='blueman-manager'),
  Match(wm_class='Conky'),
  Match(wm_class='kdeconnect-app'),
  Match(wm_class='VirtualBox Machine'),
  Match(wm_class='lxappearance'),
  Match(wm_class='qt5ct'),
  Match(wm_class='xarchiver'),
  Match(wm_class='Clamtk'),
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# Allows auto-minimize when losing focus for apps that need it
auto_minimize = True

# Functions for changing groups
def window_to_prev_group(qtile):
  if qtile.currentWindow is not None:
    i = qtile.groups.index(qtile.currentGroup)

def window_to_next_group(qtile):
  if qtile.currentWindow is not None:
    i = qtile.groups.index(qtile.currentGroup)
    qtile.currentWindow.togroup(qtile.groups[i + 1].name)

# Hooks
#Runs startup applications
@hook.subscribe.startup_once
def start_once():
  subprocess.call([home + '/.config/qtile/autostart.sh'])

# java UI toolkits/whitelist
wmname = "LG3D"
