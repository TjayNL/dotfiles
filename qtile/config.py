import os
import subprocess

from libqtile.config import Key, Screen, Group, Match, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from typing import List  # noqa: F401

mod = "mod4"

##### QTILE KEY BINDS #####
keys = [
    # Switch between windows in current stack pane
    Key([mod], "a", lazy.layout.left()),
    Key([mod], "d", lazy.layout.right()),
    Key([mod], "s", lazy.layout.down()),
    Key([mod], "w", lazy.layout.up()),

    # Switch between windows in current stack pane
    Key([mod], "p", lazy.layout.grow()),
    Key([mod], "o", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "m", lazy.layout.maximize()),
    
    # Move windows up or down in current stack
    Key([mod, "shift"], "s", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "w", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "a", lazy.layout.swap_left()),
    Key([mod, "shift"], "d", lazy.layout.swap_right()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("termite")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "q", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),


    Key([mod], "r", lazy.spawn("rofi -modi ssh,run,drun -show drun run ssh -theme flat-yellow")),

    # Programm Keybinds
    Key([mod, "control"], "c", lazy.spawn("code-oss")),
    Key([mod, "control"], "f", lazy.spawn("pcmanfm")),
    Key([mod, "control"], "b", lazy.spawn("firefox")),
    Key([mod, "control"], "s", lazy.spawn("spotify")),
    Key([mod, "control"], "v", lazy.spawn("discord")),

    # System control keybinds
    Key([mod, "control"], "p", lazy.spawn("pavucontrol")),
    Key([mod, "control"], "l", lazy.spawn("lxappearance")),


    # Commands: Volume Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn("amixer -q -c 3 sset Master 5dB+")),
    Key([], 'XF86AudioLowerVolume', lazy.spawn("amixer -q -c 3 sset 'Master' 5dB-")),
    Key([], 'XF86AudioMute', lazy.spawn("amixer -q -D pulse sset Master 1+ toggle")),
]

##### GROUPS #####
groups = [
    Group("1", label="DEV", matches=[Match(wm_class=["code-oss"])]),
    Group("2", label="WWW", matches=[Match(wm_class=["firefox"])]),
    Group('3', label="SYS", matches=[
                                    Match(wm_class=["Pcmanfm"]),
                                    ]
    ),
    Group('4', label="GAME", matches=[Match(wm_class=["Steam"])]),
    Group('5', label="OBS", matches=[Match(wm_class=["obs"])]),
    Group("6", label="CHAT", matches=[Match(wm_class=["discord"])]),
    Group("7", label="MEDIA", matches=[Match(wm_class=["Spotify"])]),
    Group("8", label="GFX", matches=[
                                    Match(wm_class=["Gimp"]),
                                    Match(wm_class=["Inkscape"]),
                                    Match(wm_class=["GravitDesigner"]),
                                    ]
    ),
]
for i in groups:
    # mod + letter of group = switch to group
    keys.append(Key([mod], i.name, lazy.group[i.name].toscreen()))

    # mod + shift + letter of group = switch to & move focused window to group
    keys.append(Key([mod, 'shift'], i.name, lazy.window.togroup(i.name)))

dgroups_key_binder = None
dgroups_app_rules = []

# Layouts
layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
    layout.tree.TreeTab(),
    layout.MonadTall(),
    layout.Floating(),
]

floating_layout = layout.Floating()

##### SCREENS & WIDGET OPTIONS #####
screens = [
    Screen(
        top=bar.Bar(
            widgets=[
                widget.GroupBox(
                    active='ffffff',
                    inactive='444444',
                    highlight_method='line',
                    highlight_color='0F0F0F',
                    this_current_screen_border='FFCD00',
                    this_screen_border='FFCD00',
                ),
                widget.Prompt(),
                widget.WindowName(
                    fontsize=15,
                ),
                widget.Spacer(
                    length=75
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    padding=0,
                    foreground="FFCD00"
                ),
                widget.Net(
                    interface="enp4s0",
                ),
                widget.Spacer(
                    length=10
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    #text=(""),
                    padding=0,
                    foreground="FFCD00"
                ),
                widget.CPUGraph(
                    type="linefill",
                    line_width=1,
                    graph_color="FFCD00",
                    fill_color="FFCD00.3",
                    border_color="0F0F0F",
                ),
                widget.Spacer(
                    length=10
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    padding=0,
                    foreground="FFCD00"
                ),
                widget.Memory(
                    fmt="{MemUsed}M",
                    update_interval=10,
                ),
                #widget.MemoryGraph(
                #    type="linefill",
                #    line_width=1,
                #    graph_color="FFCD00",
                #    fill_color="FFCD00.3",
                #    border_color="000000",
                #),
                widget.Spacer(
                    length=10
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    padding=0,
                    foreground="FFCD00"
                ),
                widget.ThermalSensor(),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    padding =5,
                    foreground="FFCD00"
                ),
                widget.Pacman(
                    execute="termite",
                    update_interval=1800,
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    foreground="FFCD00"
                ),
                widget.CurrentLayout(),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    foreground="FFCD00"
                ),
                widget.Volume(
                    device='default'
                ),
                widget.Spacer(
                    length=5
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    padding=0,
                    foreground="FFCD00"
                ),
                widget.Clock(
                    format='%a %d %b - %H:%M'
                ),
                widget.Spacer(
                    length=5
                ),
                widget.Systray(
                    icon_size=16,
                ),
                widget.Spacer(
                    length=10
                ),
            ],
            size=30,
            background='0F0F0F',
        ),
    ),
]

widget_defaults = dict(
    font='Ubuntu',
    fontsize=11,
)

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    #{'wmclass': 'pavucontrol'},
])
auto_fullscreen = True
focus_on_window_activation = "smart"


##### STARTUP APPLICATIONS #####

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

wmname = "qtile"
