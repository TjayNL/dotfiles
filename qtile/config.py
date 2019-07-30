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
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

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
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    ##### CUSTOM KEYBINDS #####
    Key([mod, "shift"], "c", lazy.spawn("code-oss")),
    Key([mod, "shift"], "f", lazy.spawn("firefox")),
    Key([mod, "control"], "s", lazy.spawn("spotify")),
    Key([mod, "shift"], "s", lazy.spawn("pavucontrol")),


    # Commands: Volume Controls
    #Key([], 'XF86AudioRaiseVolume', lazy.spawn("amixer -q -c 1 sset Master 5dB+")),
    #Key([], 'XF86AudioLowerVolume', lazy.spawn("amixer -q -c 1 sset Master 5dB-")),
    Key([], 'XF86AudioMute', lazy.spawn("amixer -q -D pulse sset Master 1+ toggle")),
]

##### GROUPS #####
groups = [
    Group("1", label="DEV", matches=[Match(wm_class=["code-oss"])]),
    Group("2", label="WWW", matches=[Match(wm_class=["firefox"])]),
    Group('3', label="SYS", matches=[
                                    Match(wm_class=["dolphin"]),
                                    Match(wm_class=["Thunar"]),
                                    Match(wm_class=["nautilus"]),
                                    ]
    ),
    Group('4', label="GAME", matches=[Match(wm_class=["Steam"])]),
    Group('5', label="OBS", matches=[Match(wm_class=["obs"])]),
    Group("6", label="CHAT", matches=[Match(wm_class=["discord"])]),
    Group("7", label="MEDIA", matches=[Match(wm_class=["Spotify"])]),
    Group("8", label="GFX"),
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
                    inactive='222222',
                    highlight_method='line',
                    highlight_color='000000',
                    this_current_screen_border='FFCD00',
                    this_screen_border='FFCD00',
                ),
                widget.Prompt(),
                widget.WindowName(
                    fontsize=15,
                ),
                widget.Systray(),
                widget.CPUGraph(
                    graph_color='18BAEB',
                    fill_color='FFCD00.3',
                    background='000000',
                    border_width=0,
                    border_color='000000',
                    line_width=1,
                    margin_x=0,
                    margin_y=0,
                    width=50,
                ),
                widget.MemoryGraph(
                    graph_color='00FE81',
                    fill_color='00B25B.3',
                    background='000000',
                    border_width=0,
                    border_color='000000',
                    line_width=1,
                    margin_x=0,
                    margin_y=0,
                    width=50,
                ),
                widget.Memory(
                    fmt="{MemUsed}M",
                    update_interval=10,
                    background='000000'
                ),
                widget.ThermalSensor(),
                widget.Sep( linewidth=1, foreground='999999', size_percent=50 ),
                widget.CurrentLayout(),
                widget.Sep( linewidth=1, foreground='999999', size_percent=50 ),
                # widget.Volume(
                #    device='Scarlett Solo USB'
                #),
                widget.Pacman(),
                widget.Sep( linewidth=1, foreground='999999', size_percent=50 ),
                widget.Clock(
                    fontsize=12,
                    format='%a %d %b %H:%M'
                )
            ],
            size=30,
            background='000000',
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
    {'wmclass': 'pavucontrol'},
])
auto_fullscreen = True
focus_on_window_activation = "smart"


##### STARTUP APPLICATIONS #####

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

wmname = "qtile"
