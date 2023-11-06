#!/usr/bin/python3

# colors.py
# Adapted from: Peter Mortensen (via Stack Overflow <https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal>)
# 2021-01-03

import re

class style:
    '''Colors class:
    Reset all colors with colors.reset
    Two subclasses fg for foreground and bg for background.
    Use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    Also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    italic = '\033[03m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    fg = {
      'black': '\033[30m',
      'red': '\033[31m',
      'green': '\033[32m',
      'orange': '\033[33m',
      'blue': '\033[34m',
      'purple': '\033[35m',
      'cyan': '\033[36m',
      'lightgrey': '\033[37m',
      'darkgrey': '\033[90m',
      'lightred': '\033[91m',
      'lightgreen': '\033[92m',
      'yellow': '\033[93m',
      'lightblue': '\033[94m',
      'pink': '\033[95m',
      'lightcyan': '\033[96m'
    }
    bg = {
        'black': '\033[40m',
        'red': '\033[41m',
        'green': '\033[42m',
        'orange': '\033[43m',
        'blue': '\033[44m',
        'purple': '\033[45m',
        'cyan': '\033[46m',
        'lightgrey': '\033[47m',
        'yellow': '\033[103m',
    }
def hex2rgb(h):
  h = h.strip().replace('#', '')
  r,g,b = [int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
  return "{},{},{}".format(r,g,b)

def rgb2hex(rgb):
  r,g,b = rgb.split(',')
  return '#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))

def rgb(text, r=255, g=255, b=255):
  return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def font_style(text, fstyle):
  if 'bold' in fstyle:
    return style.reset + style.bold + text + style.reset
  if 'italic' in fstyle:
    return style.reset + style.italic + text + style.reset
  if 'underline' in fstyle:
    return style.reset + style.underline + text + style.reset

def apply_fg(text, colorin):
  if '#' in colorin:
    colorin = hex2rgb(colorin)
  if ',' in colorin:
    r,g,b = colorin.split(',')
    return f"\033[38;2;{r};{g};{b}m" + text + style.reset
  return style.reset + style.fg[colorin] + text + style.reset

def apply_bg(text, colorin):
  if '#' in colorin:
    colorin = hex2rgb(colorin)
  if ',' in colorin:
    r,g,b = colorin.split(',')
    return f"\033[48;2;{r};{g};{b}m{text}\033[0m"
  return style.reset + style.bg[colorin] + text + style.reset

def apply_fg_bg(text, fg, bg):
  if '#' in fg:
    fg = hex2rgb(fg)
    bg = hex2rgb(bg)
  if ',' in fg:
    fr,fg,fb = fg.split(',')
    br,bg,bb = bg.split(',')
    fg = f"\033[38;2;{fr};{fg};{fb}m" #FG
    bg = f"\033[48;2;{br};{bg};{bb}m{text}\033[0m" #BG
    return fg + bg
  return style.reset + style.fg[fg] + style.bg[bg] + text + style.reset

def highlight(text):
  ''' Highlights text in yellow '''
  return apply_fg_bg(text, 'black', 'yellow')

def highlight_first_match(needle, haystack):
  if needle.lower() in haystack.lower():
    start = haystack.lower().index(needle.lower())
    end = start + len(needle)
    word = haystack[start:end]
    return haystack[0:start] + highlight(word) + haystack[end:]
  return haystack

def highlight_match(needle, haystack):
  if needle.lower() in haystack.lower():
    regex = r'(' + re.escape(needle) + r')'
    return re.sub(regex, highlight(r'\1'), haystack, re.I)
  return haystack

def error(text):
  print(style.reset + style.bold + style.fg['red'] + text + style.reset)

def __echo(text, colorin='0,0,0'):
  ''' Prints with a specific foreground color '''
  if '#' in colorin:
    colorin = hex2rgb(colorin)
  if ',' in colorin:
    colorin = colorin.replace('rgb(','').replace(')','').replace(' ','')
    c = colorin.split(',')
    print(style.reset + rgb(text, c[0],c[1],c[2])  + style.reset)
  elif 'bold' in colorin:
    print(style.reset + style.bold + text + style.reset)
  elif 'underline' in colorin:
    print(style.reset + style.underline + text + style.reset)
  elif 'ul' in colorin:
    print(style.reset + style.underline + text + style.reset)
  elif colorin in style.fg:
    print(style.reset + style.fg[colorin] + text + style.reset)
  else:
    print(text)

def echo(*argv):
  ''' Prints with a specific foreground color. Allows multiple values '''
  colorin = style.reset
  last_arg = argv[-1]
  if re.match(r'\d+,\d+,\d+|#[a-f0-9]|^bold$|^underline$|^ul$', last_arg, flags=re.I):
    colorin = last_arg
  if 'rgb' in last_arg:
    colorin = last_arg
  if last_arg in style.fg:
    colorin = last_arg
  __echo(' '.join(argv[0:-1]), colorin)

def echo_bg(text, colorin):
  ''' Prints with a specific background color '''
  if ',' in colorin:
    c = colorin.split(',')
    print(style.reset + rgb(text, c[0],c[1],c[2]) + style.reset)
  else:
    print(style.reset + style.bg[colorin] + text + style.reset)

def linkify(text):
  return style.reset + style.fg['blue'] + style.underline + text + style.reset

def invert(color):
  if re.match('rgb', color, flags=re.I):
    rgb = color.replace('rgb','').replace('RGB','').replace('(','').replace(')','').replace(' ','')
    color = rgb2hex(rgb)
  color = color[1:]
  color = int(color, 16)
  comp_color = 0xFFFFFF ^ color
  comp_color = "#%06X" % comp_color
  return comp_color
