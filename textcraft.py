import copy
import math
import random
import time
from functools import partial
from os.path import join

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config, ConfigParser
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.settings import Settings, SettingsWithSidebar
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle
from kivy.core.text import Label as CoreLabel
from kivy.base import runTouchApp

from jsonsettings import json_settings
testing = False

splash = """
     TEXTCRAFT Alpha 0.1
      Sam Stoltenberg
"""
sm = ScreenManager(transition=NoTransition())
main_text = ''

# Bugs
    # future error, lol  burning enchanted wooden tools,
    # won't be able to select which wood tool to burn

def alert(msg):
    """Takes a message and displays a popup for it"""
    _var_msg = msg
    if 'pickaxe' in msg:
        _var_msg = str('Your %s\nhas broken!' % current_pickaxe[0])
        _var_msg = _var_msg.replace('_', ' ')
    elif 'axe' in msg:
        _var_msg = str('Your %s\nhas broken!' % current_axe[0])
        _var_msg = _var_msg.replace('_', ' ')
    elif 'shovel' in msg:
        _var_msg = str('Your %s\nhas broken!' % current_shovel[0])
        _var_msg = _var_msg.replace('_', ' ')
    elif 'sword' in msg:
        _var_msg = str('Your %s\nhas broken!' % current_sword[0])
        _var_msg = _var_msg.replace('_', ' ')
    elif 'helmet' in msg:
        _var_msg = str('Your %s\nhas broken!' % current_helmet[0])
        _var_msg = _var_msg.replace('_', ' ')
    elif 'chestplate' in msg:
        _var_msg = str('Your %s\nhas broken!' % current_chestplate[0])
        _var_msg = _var_msg.replace('_', ' ')
    elif 'leggings' in msg:
        _var_msg = str('Your %s\nhas broken!' % current_leggings[0])
        _var_msg = _var_msg.replace('_', ' ')
    elif 'boots' in msg:
        _var_msg = str('Your %s\nhas broken!' % current_boots[0])
        _var_msg = _var_msg.replace('_', ' ')
    global alertx_label
    alertx_label = AlertWindow()
    alertx_label.text = str(_var_msg)
    Window.add_widget(alertx_label)

def alertf(msg):
    _var_msg = msg
    global alertx_label
    alertx_label = AlertWindow()
    alertx_label.text = str(_var_msg)
    Window.add_widget(alertx_label)

def testbtn_callback(self):
        sm.switch_to(Testing())

# statcheck use with sc('tree', 'logs')
def sc(family, stat):
    x = 0
    for i in stats:
        if i[0] == family:
            for j in i[1]:
                if j == stat:
                    return(i[1][x+1])
                x += 1
            return 0

class Engine(object):

    def __init__(self):
        pass

    # Stores x, y times
    def store(self, x, y):
        print(x, y)
        global equipment
        if y > 0:
            stat.item(x, y)
        y = int(y)
        # ['stick', 'wood_plank', 2, 4]
        # ['fishing_rod', 'stick', 3, 'string', 2, 1]]
        # x is the item to add
        # y is the quanity
        # This is how all items are stored into the inventory
        added = False
        in_tools = False
        item_deleted = False
        z = 0
        remove = 0
        tools2 = copy.deepcopy(tools)
        for i in tools2:
            if x == i[0]:
                if y > 0:
                    while y > 0:
                        equipment.append(i)
                        in_tools = True
                        y -= 1

                elif not in_tools:
                    for i in equipment:
                        if i[0] == x and not item_deleted:
                            item_deleted = True
                            equipment.remove(i)
                            in_tools = True

        if not in_tools:
            for i in inventory:
                if i[0] == x:
                    i[1] = i[1] + y
                    added = True

            if not added:
                inventory.append([x, y])

    # Checking the clock or moving time forward
    def tick(self, x):
        # tick(0) checks the clock
        # tick(x) checks clock and moves time forward by x
        global clock
        global night
        print('time', clock)
        if x == 0:
            if clock < 50:
                night = False
                return ("  Birds are singing in the sunlight...\n")
            else:
                night = True
                return ("  Crickets are chirping in the moonlight...\n")

        # For sleeping
        elif x == 100:
            clock = 0
            night = False
            msg = ''
            msg += ("=========================\n")
            msg += ("=========================\n")
            msg += ("The sun has RISEN!\n")
            msg += ("=========================\n")
            msg += ("=========================\n")
            alertf(msg)

        else:
            clock += x
            if clock >= 50 and night == False:
                night = True
                msg = ''
                msg += ("=========================\n")
                msg += ("=========================\n")
                msg += ("The sun has FALLEN!\n")
                msg += ("=========================\n")
                msg += ("=========================\n")
                alertf(msg)
            if clock >= 100:
                night = False
                msg = ''
                msg += ("=========================\n")
                msg += ("=========================\n")
                msg += ("The sun has RISEN!\n")
                msg += ("=========================\n")
                msg += ("=========================\n")
                clock = 0
                alertf(msg)

    def money_add(self, x):
        # add achievement here for negatives
        # spending money :)
        global money
        money += x

    def save(object):
        global night
        global furnace_have
        global health
        global wolves
        global clock
        global money
        global current_pickaxe
        global user_id
        global current_shovel
        global current_axe
        global current_helmet
        global current_chestplace
        global current_leggings
        global current_boots
        global current_sword
        global current_time
        global furnace_level
        global time_left_cooking
        global is_cooking
        global farming_started
        global time_passed_storm
        global cooking_chart
        global stats
        current_time = math.floor(time.time())
        base = []
        base.append(night)
        base.append(furnace_have)
        base.append(health)
        base.append(wolves)
        base.append(clock)
        base.append(money)
        base.append(current_pickaxe)
        base.append(user_id)
        base.append(current_shovel)
        base.append(current_axe)
        base.append(current_helmet)
        base.append(current_chestplate)
        base.append(current_leggings)
        base.append(current_boots)
        base.append(current_sword)
        base.append(current_time)
        base.append(furnace_level)
        base.append(time_left_cooking)
        base.append(is_cooking)
        base.append(farming_started)
        base.append(time_passed_storm)
        base.append(cooking_chart)
        store_file.put('inventory', content=inventory)
        store_file.put('all_farms', content=all_farms)
        store_file.put('equipment', content=equipment)
        store_file.put('achievements_list', content=achievements_list)
        store_file.put('base', content=base)
        store_file.put('stats', content=stats)

    def version(object):
        pass

    def dead(self):
        global death_message
        global night
        global furnace_have
        global health
        global wolves
        global clock
        global money
        global equipment
        global current_pickaxe
        global user_id
        global current_shovel
        global current_axe
        global current_helmet
        global current_chestplate
        global current_leggings
        global current_boots
        global current_sword
        global current_time
        global furnace_level
        global time_left_cooking
        global is_cooking
        global farming_started
        global time_passed_storm
        global cooking_chart
        global achievements_list
        global inventory
        global all_farms
        global base
        Clock.unschedule(FarmEngine.interval)
        Clock.unschedule(engine.count_down)
        # [variable ,Don't have have 0 or 1 ,goal ,
        # "achievement",reason for achievement]
        achievements_list = [
            [0, 0, 'Dirt Miner', 100, 'mining 100 dirt'],  # 0
            [0, 0, 'Dirty Diamonds', 2, 'mining 2 diamonds'],  # 1
            [0, 0, 'Tree Hugger(not)', 50, 'killing 50 trees'],  # 2
            [0, 0, 'Cover Me Feet', 1, 'pouring water on lava (not dying)'],
            [0, 0, 'Sorry, Mom', 1, 'killing a cow'],  # 4
            [0, 0, 'Jill', 20, 'filling your bucket 20 times'],  # 5
            [0, 0, 'Good morning, ladies', 10, 'catching 10 fish'],  # 6
            [0, 0, 'Bitch Tamer', 5, 'taming 5 wolves'],  # 7
            [0, 0, 'Dar3 D3vil', 10, 'killing 10 creepers'],  # 8
            [0, 0, 'Worrisome', 100, 'opening inventory 100 times'],  # 9
            [0, 0, 'Oink, Oink', 100, 'eat 100 items']  # 10
            # 11 millionaire
        ]
        current_time = (math.floor(time.time()))
        inventory = [['torch', 1]]
        all_farms = []
        base = [0, 0, 100, 0, 0, 0,
            ['fist',-1, 0, -1, .5], 'user_id',
            ['fist', -1, 0, -1, .5],
            ['fist', -1, 0, -1, .5],
            ['skin', -1, 0, -1, 1],
            ['skin', -1, 0, -1, 1],
            ['skin', -1, 0, -1, 1],
            ['skin', -1, 0, -1, 1],
            ['fist', -1, 0, -1, .5],
            current_time, 1, 0, False, False, 0, []]
        equipment = []

        height = 64
        night = base[0]
        furnace_have = base[1]
        health = base[2]
        wolves = base[3]
        clock = base[4]
        money = base[5]
        current_pickaxe = base[6]
        user_id = base[7]
        current_shovel = base[8]
        current_axe = base[9]
        current_helmet = base[10]
        current_chestplate = base[11]
        current_leggings = base[12]
        current_boots = base[13]
        current_sword = base[14]
        current_time = base[15]
        furnace_level = base[16]
        time_left_cooking = base[17]
        is_cooking = base[18]
        farming_started = base[19]
        time_passed_storm = base[20]
        cooking_chart = base[21]
        engine.save()
        sm.add_widget(Death(name='dead'))
        sm.switch_to(Death())

    def count_down(self, dt):
        global cooking_chart
        global time_left_cooking
        global is_cooking
        global furnace_level
        a = cooking_chart
        material = a[0]
        material_quantity = a[1]
        fuel = a[2]
        fq = a[3]
        if not is_cooking:  # first time cooking defines time
            is_cooking = True
            time_left_cooking = int(3 * (1/float(furnace_level)) * material_quantity)
            # 3 * 1 / furnace_level * material
        if time_left_cooking == 0:
            _double = 1
            if random.randint(0, 100) < (furnace_level * 2):
                _double = 2
            for i in cook_output:
                if material == i[0]:
                    gained_material = i[1]
            engine.store(gained_material, material_quantity)
            stat.cook(gained_material, material_quantity)
            is_cooking = False
            Clock.unschedule(engine.count_down)
            # add images, if x material, put x image comment line
            # comment line in engine.count_down
            tmaterial = gained_material.replace("_", " ")
            # done_cooking_button.text = 
            alertf(str(('Your %s %s\n' +
                                            'has cooked\n' +
                                            'using %s %s.') % (
                                            material_quantity,
                                            tmaterial,
                                            fq, fuel.replace('_', ' '))))
            #done_cooking_popup.open()
        else:
            time_left_cooking -= 1

    def close_popup(self, popup):
        popup.dismiss()

    # When unequipping something, ...
    # if it's not a fist or skin, puts back in inventory
    def old_equipment(self, x):
        if x[0] == 'fist' or x[0] == 'skin':
            pass
        else:
            equipment.append(x)

# command example  stat.ore('obsidian', 20)
class Stat(object):

    # add to adventure
    def animal(self, material, quantity):
        if material == 'cow':
            achievements_list[4][0] += 1
        elif material == 'creeper':
            achievements_list[8][0] += 1
        stat.add(material, quantity, 'animal')

    def ore(self, material, quantity):
        if material == 'diamond':
            achievements_list[1][0] += 1
        elif material == 'dirt':
            achievements_list[0][0] += 1
        stat.add(material, quantity, 'ore')

    def tree(self, material, quantity):
        if material == 'tree':
            achievements_list[2][0] += 1
        stat.add(material, quantity, 'tree')

    def craft(self, material, quantity):
        stat.add(material, quantity, 'craft')

    def cook(self, material, quantity):
        stat.add(material, quantity, 'cook')
    
    def harvest(self, material, quantity):
        stat.add(material, quantity, 'harvest')

    def item(self, material, quantity):
        stat.add(material, quantity, 'item')

    def misc(self, material, quantity):
        if material == 'open_inv':
            achievements_list[9][0] += 1
        elif material == 'eat':
            achievements_list[10][0] += 1
        elif material == 'fish_caught':
            achievements_list[6][0] += 1
        elif material == 'wolf_tamed':
            achievements_list[7][0] += 1
        elif material == 'bucket_filled':
            achievements_list[5][0] += 1
        elif material == 'lava_blocked':
            achievements_list[3][0] += 1
        stat.add(material, quantity, 'misc')

    def add(self, material, quantity, family):
        global stats
        z = 0
        added = False
        for i in stats:
                if i[0] == family:
                    for j in i[1]:
                        z += 1
                        if material == j:
                            added = True
                            i[1][z] = int(i[1][z]) + quantity
                    if not added:
                        i[1].append(material)
                        i[1].append(quantity)
        self.check_achieve()
        engine.save()

    def check_achieve(self):
        for i in achievements_list:
            if i[0] >= i[3] and i[1] == 0:
                i[1] = 1
                alert("You gained %s achievement" % i[2])
        

class HealthBar(ProgressBar):

    def __init__(self, **kwargs):
        super(HealthBar, self).__init__(**kwargs)
        global health
        self.value = health
        self.label = CoreLabel(
            text='Health',
            font_size=Window.height/16)
        self.texture_size = None
        self.refresh_text()
        self.draw()

    def draw(self):

        with self.canvas:
            self.canvas.clear()

            # Draw no progress bar
            Color(.188, .209, .148)
            RoundedRectangle(
                pos=self.pos,
                size=self.size)

            Color(.5, 0, 0)
            if self.value > 0:
                var = 100.0/self.value
                # Draw progress bar
                RoundedRectangle(
                    pos=self.pos,
                    size=(self.width/var, self.height))
            # Center and draw the text
            Color(1, 1, 1, 1)
            RoundedRectangle(texture=self.label.texture, size=self.texture_size,
                pos=(self.size[0]/2 - self.texture_size[0]/2, self.size[1]/2 - self.texture_size[1]/2))

    def refresh_text(self):
        # Render the label
        self.label.refresh()

        # Set the texture size each refresh
        self.texture_size = list(self.label.texture.size)

    def set_value(self, value):
        self.value = value
        self.refresh_text()
        self.draw()


class EquipmentBar(ProgressBar):

    def __init__(self, **kwargs):
        super(EquipmentBar, self).__init__(**kwargs)
        self.label = CoreLabel(
            text=self.text,
            font_size=Window.height/16)
        self.texture_size = None
        self.refresh_text()
        self.draw()

    def draw(self):

        with self.canvas:
            self.canvas.clear()

            # Draw no progress bar
            Color(.5, 0, 0)
            RoundedRectangle(
                pos=self.pos,
                size=self.size)
            Color(0, .65, 0)

            if self.value > 0:
                var = 100.0/self.value
                # Draw progress bar
                RoundedRectangle(
                    pos=self.pos,
                    size=(self.width/var, self.height))
            # Center and draw the text
            Color(1, 1, 1, 1)
            RoundedRectangle(texture=self.label.texture, size=self.texture_size,
                pos=(self.size[0]/2 - self.texture_size[0]/2, self.size[1]/2 - self.texture_size[1]/2))

    def refresh_text(self):
        # Render the label
        self.label.refresh()

        # Set the texture size each refresh
        self.texture_size = list(self.label.texture.size)

    def set_value(self, value):
        self.value = value
        self.refresh_text()
        self.draw()


class AlertWindow(Label):
    def __init__(self, **kwargs):
        super(AlertWindow, self).__init__(**kwargs)
        self.font_size = '45dp'
        self.pos = [0, -300]
        self.color = ([.42, .77, .92, 1])
        Clock.schedule_interval(self.move, .01)

    def move(self, dt):
        self.pos[1] += 2.5
        if self.pos[1] >= 350:
            Clock.unschedule(self.move)
            Window.remove_widget(alertx_label)


class InvBtn(Button):
    def __init__(self, **kwargs):
        super(InvBtn, self).__init__(**kwargs)
        self.font_size = '40dp'
        self.size_hint=(.4, .4)


class Inv(Screen):
    def __init__(self, **kwargs):
        super(Inv, self).__init__(**kwargs)
        inventory.sort()
        global health
        global equipment
        self.selected_event = None
        self.selected_item = None
        self.selected_quantity = None
        self.added = 0
        self.bind(on_enter=self.build)
        self.scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height),
            pos_hint={'center_x': .5},
            bar_color=([.81, .55, .55, 1]),  #
            bar_inactive_color=([.55, .17, .17, 1]))  #
        self.grid = GridLayout(
            size_hint=(None, 2),
            cols=2
        )
        self.btn1 = Button(
            text='Trash',
            font_size='50dp',
            color=(0, 0, 0, 1),
            background_normal="btnimg/trash.jpg",
            size_hint=(None, None),
            height=int(Window.height)/6,
            width=int(Window.width)/4,
            pos_hint={'center_x': .1}
        )
        self.btn1.bind(on_press=self.trash)

        self.btn2 = Button(
            text='Equip',
            font_size='50dp',
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            height=int(Window.height)/6,
            width=int(Window.width)/2,
            pos_hint={'center_x': .492}
        )
        self.btn2.bind(on_press=self.equip)

        self.btn4 = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.btn4.bind(on_press=self.main)

        self.eatbtn = Button(
            text='',
            font_size='50dp',
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            height=int(Window.height)/6,
            width=int(Window.width)/2,
            pos_hint={'center_x': .492}
        )
        self.eatbtn.bind(on_press=self.eat)
        self.label = Label(
            text='Equipment',
            font_size='40dp',
            size_hint_x=None,
            # height=self.minimum_height,
            width=Window.width/2.22,
            #background_color=(0, 0, 0, 1)
        )
        self.label2 = Label(
            text='Equipment bar image',
            font_size='40dp',
            size_hint_x=None,
            # Equipment bar image!!
            # height=self.minimum_height,
            width=Window.width/2.22,
            #background_color=(0, 0, 0, 1)
        )
        self.scroll.scroll_y = Inv.scroll_pos
        for i in inventory:
            if i[1] <= 0:
                inventory.remove(i)
            else:
                self.added += 1
                bstext = str('%s  %s' % (i[1], i[0]))
                bstext = bstext.replace("_", " ")
                self.btn = InvBtn()
                self.btn.text = bstext
                self.btn.bind(on_press=self.callback)
                self.btn.item = i[0]
                self.btn.quantity = i[1]
                self.grid.add_widget(self.btn)
        if self.added % 2 == 1:
            self.btn = Button(
                text='',
                size_hint=(.4, .4),
                background_color=(0, 0, 0, 1)
            )
            self.grid.add_widget(self.btn)

        self.grid.add_widget(self.label)
        self.grid.add_widget(self.label2)

        for i in equipment:
            self.added += 1
            bstext = str('%s' % i[0])
            bstext = bstext.replace("_", " ")
            self.btn = InvBtn()
            self.btn.text = bstext
            self.btn.bind(on_press=self.equip_callback)
            self.btn.item = i
            self.btn.quantity = 1
            # THIS IS WHERE YOU ADD THE DURABILITY % BAR in inv screen
            self.grid.add_widget(self.btn)

        for i in range(6):
            self.btn = Button(
                text='',
                size_hint=(.4, .4),
                background_color=(0, 0, 0, 1)
            )
            self.grid.add_widget(self.btn)

        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)
        self.add_widget(self.btn1)
        self.add_widget(self.btn4)

    def build(self, event):
        stat.misc("open_inv", 1)

    def equip_callback(self, event):
        self.remove_widget(self.btn2)
        self.add_widget(self.btn2)
        self.selected_item = event.item
        self.selected_quantity = event.quantity
        try:
            self.selected_event.background_color = (1, 1, 1, 1)
        except AttributeError:
            pass
        self.selected_event = event
        event.background_color = (1, 0, 1, 1)

    def callback(self, event):
        global health
        self.selected_item = event.item
        self.selected_quantity = event.quantity
        try:
            self.selected_event.background_color = (1, 1, 1, 1)
        except AttributeError:
            pass
        self.edible = False
        self.remove_widget(self.eatbtn)
        for i in edible:
            if self.selected_item == i[0]:
                try:
                    self.remove_widget(self.btn2)
                    self.add_widget(self.eatbtn)
                    self.eatbtn.bind(on_press=self.eat)
                    if health == 100:
                        self.eatbtn.text = 'Health Full'
                    else:
                        self.eatbtn.text = 'Eat'
                except Exception:
                    pass
                self.edible = True
        if self.selected_item in tools:
            self.remove_widget(self.btn2)
            self.add_widget(self.btn2)
        self.selected_event = event
        event.background_color = (1, 0, 1, 1)

    def eat(self, event):
        global health
        global death_message
        stat.misc("eat", 1)
        engine.store(self.selected_item, -1)
        self.selected_quantity -= 1
        if self.selected_quantity == 0:
            Inv.scroll_pos = self.scroll.scroll_y
            sm.switch_to(Inv())
            # need more code here
        else:
            self.eatbtn.bind(on_press=self.eat)
        for i in inventory:
            if i[0] == self.selected_item:
                eattext = str('%s  %s' % (i[1], i[0]))
                eattext = eattext.replace("_", " ")
                self.selected_event.text = eattext
                if self.selected_item in semi_edible:
                    if random.randint(0, 100) < 70:
                        self.eatbtn.text = 'Ehh...'
                        self.eat_item()
                    else:
                        self.eatbtn.text = 'Yuck...'
                        health -= 10
                        if health <= 0:
                            death_message = 'You die of a\nmysterious sickness'
                            engine.dead()

                else:
                    self.eatbtn.text = 'Yum!'
                    self.eat_item()

    def eat_item(self):
        global health
        for i in edible:
            if i[0] == self.selected_item:
                health += i[1]
        if health > 100:
            health = 100
        if health == 100:
            self.eatbtn.text = 'Health Full'

    def passed(self, event):
        pass

    def trash(self, event):
        if self.selected_item != None and self.selected_item not in tools:
            #self.remove_widget(self.selected_event)
            engine.store(self.selected_item, -self.selected_quantity)
            Inv.scroll_pos = self.scroll.scroll_y
            sm.switch_to(Inv())
        elif self.selected_item != None:
            #self.remove_widget(self.selected_event)
            engine.store(self.selected_item[0], -self.selected_quantity)
            Inv.scroll_pos = self.scroll.scroll_y
            sm.switch_to(Inv())

    def equip(self, event):
        global picks
        global shovels
        global axes
        global swords
        global helmets
        global chestplates
        global leggings
        global boots
        global current_pickaxe
        global current_shovel
        global current_axe
        global current_sword
        global current_helmet
        global current_chestplate
        global current_leggings
        global current_boots
        _item = self.selected_item
        _item[0] = _item[0].replace(" ", "_")
        if 'pickaxe' in _item[0]:
            engine.store(_item[0], -1)
            engine.old_equipment(current_pickaxe)
            current_pickaxe = _item

        elif 'axe' in _item[0]:
            engine.store(_item[0], -1)
            engine.old_equipment(current_axe)
            current_axe = _item

        elif 'shovel' in _item[0]:
            engine.store(_item[0], -1)
            engine.old_equipment(current_shovel)
            current_shovel = _item

        elif 'sword' in _item[0]:
            engine.store(_item[0], -1)
            engine.old_equipment(current_sword)
            current_sword = _item

        elif 'helmet' in _item[0]:
            engine.store(_item[0], -1)
            engine.old_equipment(current_helmet)
            current_helmet = _item

        elif 'chestplate' in _item[0]:
            engine.store(_item[0], -1)
            engine.old_equipment(current_chestplate)
            current_chestplate = _item

        elif 'leggings' in _item[0]:
            engine.store(_item[0], -1)
            engine.old_equipment(current_leggings)
            current_leggings = _item

        elif 'boots' in _item[0]:
            engine.store(_item[0], -1)
            engine.old_equipment(current_boots)
            current_boots = _item
        Inv.scroll_pos = self.scroll.scroll_y
        sm.switch_to(Inv())

    def main(self, event):
        Inv.scroll_pos = 1
        sm.switch_to(MainScreen())


class Equip(Screen):
    def __init__(self, **kwargs):
        super(Equip, self).__init__(**kwargs)
        _current = []
        _current.append(current_helmet)
        _current.append(current_chestplate)
        _current.append(current_leggings)
        _current.append(current_boots)
        _current.append(current_sword)
        _current.append(current_shovel)
        _current.append(current_pickaxe)
        _current.append(current_axe)
        # to fix the buttons, add scrollview to relative
        # and add the buttons to relative
        # or just remove scrollview, since it can all fit on
        # the screen
        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit_screen)
        self.add_widget(self.exitbtn)
        scrollview = ScrollView()

        self.grid = GridLayout(cols=1)
        for i in _current:
            if i[0] != 'fist' and i[0] != 'skin':
                relate = GridLayout(cols=1, size_hint=(None, None), size=(Window.width, Window.height/11))
                relate2 = RelativeLayout()
                bstext = i[0].replace('_', ' ')
                EquipmentBar.text='%s' % bstext
                percentage = math.ceil(100 * (i[1]) / i[3])
                label = EquipmentBar(
                    size_hint=(None, None),
                    max=100,
                    height=Window.height/12.0,
                    width=Window.width
                )
                label.set_value(percentage)
                relate2.add_widget(label)
                label2 = Label(
                    size_hint=(None,None),
                    height=5)
              
                self.grid.add_widget(label2)
                
                self.btn = Button(
                        text='Unequip',
                        font_size='25dp',
                        size_hint=(None, None),
                        height=Window.height/20.0,
                        width=Window.width/6.0,
                        pos_hint={'center_y': .4, 'center_x': .1})
                self.btn.item = i
                self.btn.bind(on_press=self.unequip)
                relate2.add_widget(self.btn)
                relate.add_widget(relate2)
                self.grid.add_widget(relate)
        label3 = Label(
            size_hint=(None,None),
            height=5)
        self.grid.add_widget(label3)
        gridz = GridLayout(cols=2)
        gridz.add_widget(Label(size_hint_x=None,
                         width=int(Window.width/4.0)))
        self.btn3 = Button(
            text='Equip Best',
            font_size='50dp',
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            pos_hint={'center_x': .5},
            height=int(Window.height)/5.0,
            width=int(Window.width)/2.0
            )
        gridz.add_widget(self.btn3)
        self.btn3.bind(on_press=self.equip_best)
        self.maingrid = GridLayout(cols=1)
        self.maingrid.add_widget(self.grid)
        self.maingrid.add_widget(gridz)
        self.add_widget(self.maingrid)
        
    def unequip(self, event):
        global picks
        global shovels
        global axes
        global swords
        global helmets
        global chestplates
        global leggings
        global boots
        global current_pickaxe
        global current_shovel
        global current_axe
        global current_sword
        global current_helmet
        global current_chestplate
        global current_leggings
        global current_boots
        global equipment
        _item = event.item
        if 'pickaxe' in _item[0]:
            engine.old_equipment(current_pickaxe)
            current_pickaxe = ['fist', -1, 0, -1, .5]

        elif 'axe' in _item[0]:
            engine.old_equipment(current_axe)
            current_axe = ['fist', -1, 0, -1, .5]

        elif 'shovel' in _item[0]:
            engine.old_equipment(current_shovel)
            current_shovel = ['fist', -1, 0, -1, .5]

        elif 'sword' in _item[0]:
            engine.old_equipment(current_sword)
            current_sword = ['fist', -1, 0, -1, .5]

        elif 'helmet' in _item[0]:
            engine.old_equipment(current_helmet)
            current_helmet = ['skin', -1, 0, -1, 1]

        elif 'chestplate' in _item[0]:
            engine.old_equipment(current_chestplate)
            current_chestplate = ['skin', -1, 0, -1, 1]

        elif 'leggings' in _item[0]:
            engine.old_equipment(current_leggings)
            current_leggings = ['skin', -1, 0, -1, 1]

        elif 'boots' in _item[0]:
            engine.old_equipment(current_boots)
            current_boots = ['skin', -1, 0, -1, 1]
        sm.switch_to(Equip())

    def equip_best(self, event):
        global picks
        global shovels
        global axes
        global swords
        global helmets
        global chestplates
        global leggings
        global boots
        global current_pickaxe
        global current_shovel
        global current_axe
        global current_sword
        global current_helmet
        global current_chestplate
        global current_leggings
        global current_boots
        x = 0
        while x != 300:
            x += 1
            for i in equipment:
                if 'pickaxe' in i[0]:
                    if i[4] > current_pickaxe[4]:
                        engine.store(i[0], -1)
                        engine.old_equipment(current_pickaxe)
                        current_pickaxe = i

                elif 'axe' in i[0]:
                    if i[4] > current_axe[4]:
                        engine.store(i[0], -1)
                        engine.old_equipment(current_axe)
                        current_axe = i

                elif 'shovel' in i[0]:
                    if i[4] > current_shovel[4]:
                        engine.store(i[0], -1)
                        engine.old_equipment(current_shovel)
                        current_shovel = i

                elif 'sword' in i[0]:
                    if i[4] > current_sword[4]:
                        engine.store(i[0], -1)
                        engine.old_equipment(current_sword)
                        current_sword = i

                elif 'helmet' in i[0]:
                    if i[4] > current_helmet[4]:
                        engine.store(i[0], -1)
                        engine.old_equipment(current_helmet)
                        current_helmet = i

                elif 'chestplate' in i[0]:
                    if i[4] > current_chestplate[4]:
                        engine.store(i[0], -1)
                        engine.old_equipment(current_chestplate)
                        current_chestplate = i

                elif 'leggings' in i[0]:
                    if i[4] > current_leggings[4]:
                        engine.store(i[0], -1)
                        engine.old_equipment(current_leggings)
                        current_leggings = i

                elif 'boots' in i[0]:
                    if i[4] > current_boots[4]:
                        engine.store(i[0], -1)
                        engine.old_equipment(current_boots)
                        current_boots = i
        sm.switch_to(Equip())

    def exit_screen(self, event):
        main_text = 'Back from Equipment...'
        sm.switch_to(MainScreen())


class CaveScreen(Screen):
    def __init__(self, **kwargs):
        super(CaveScreen, self).__init__(**kwargs)
        # health bar
        self.health = HealthBar(
            size_hint=(None, None),
            width=Window.width/2,
            height=Window.height/10
        )
        self.health_relative = RelativeLayout(
            size_hint=(None, None),
            pos_hint={'center_x': .33, 'center_y': .9}
        )
        self.health_relative.add_widget(self.health)
        self.add_widget(self.health_relative)
        # health bar
        self.looping = True
        self.ore = None
        self.mob = None
        self.mob_stat = None
        self.var_height = 60
        self.main_label = Label(
            text='The cave is large\n and unforgiving',
            font_size='35dp',
            size_hint=(None, None),
            height=int(Window.height)/6.0,
            width=int(Window.width)/4.0,
            pos_hint={'center_x': .5, 'center_y': .5}

        )
        self.add_widget(self.main_label)

        self.deepbtn = Button(
            text='Light a torch',
            font_size='40dp',
            size_hint=(None, None),
            width=int(Window.width)/3,
            height=int(Window.height)/7.5,
            pos_hint={'right': .9, 'center_y': .05}
        )
        self.deepbtn.bind(on_press=self.deep_callback)
        self.add_widget(self.deepbtn)

        self.climbbtn = Button(
            text='Turn back',
            font_size='40dp',
            size_hint=(None, None),
            width=int(Window.width)/3,
            height=int(Window.height)/7.5,
            pos_hint={'right': .4, 'center_y': .05}
        )
        self.climbbtn.bind(on_press=self.climb_out)
        self.add_widget(self.climbbtn)

        self.minebtn = Button(
            text='Mine',
            font_size='75dp',
            size_hint=(None, None),
            height=int(Window.height)/5.0,
            width=int(Window.width)/2.0,
            pos_hint={'center_x': .5, 'center_y': .29}
        )

        self.runbtn = Button(
            text='Run Away',
            font_size='50dp',
            size_hint=(None, None),
            height=int(Window.height)/6.0,
            width=int(Window.width)/3.0,
            pos_hint={'center_x': .5, 'center_y': .7}
        )
        self.runbtn.bind(on_press=self.run)

        self.eatbtn = Button(
            text='Eat',
            font_size='50dp',
            size_hint=(None, None),
            width=Window.width/6,
            height=Window.height/8.0,
            pos_hint={'center_x': .1, 'center_y': .86}
        )
        self.eatbtn.bind(on_press=self.eat)
        self.add_widget(self.eatbtn)

    def eat(self, event):
        global health
        global death_message
        have_food = False
        food = []
        for i in inventory:
            if i[0] in edible2:
                if i[1] > 0:
                    food.append(i)
                    have_food = True
            if i[0] in semi_edible:
                if i[1] > 0:
                    food.append(i)
                    have_food = True
        if have_food:
            stat.misc("eat", 1)
            num = random.randint(0, (len(food)-1))
            self.selected_item = food[num][0]
            self.selected_quantity = food[num][1]
            engine.store(self.selected_item, -1)
            self.selected_quantity -= 1
            for i in inventory:
                if i[0] == self.selected_item:
                    if self.selected_item in semi_edible:
                        if random.randint(0, 100) < 70:
                            self.main_label.text = 'Ehh...'
                            for i in edible:
                                if i[0] == self.selected_item:
                                    health += i[1]
                            if health > 100:
                                health = 100
                            if health == 100:
                                self.main_label.text = 'Health Full'
                        else:
                            self.main_label.text = 'Yuck...'
                            health -= 10
                            if health <= 0:
                                death_message = 'You die of a\nmysterious sickness'
                                engine.dead()

                    else:
                        self.main_label.text = 'Yum!'
                        for i in edible:
                            if i[0] == self.selected_item:
                                health += i[1]
                        if health > 100:
                            health = 100
                        if health == 100:
                            self.main_label.text = 'Health Full'
        else:
            self.main_label.text = 'No food left'
        self.health_relative.remove_widget(self.health)
        self.remove_widget(self.health_relative)
        self.health = HealthBar(
            size_hint=(None, None),
            width=Window.width/2,
            height=Window.height/10
        )
        self.health_relative.add_widget(self.health)
        self.add_widget(self.health_relative)

    def run(self, event):
        global health
        if self.mob_stat[0] == 'creeper':
            self.main_label.text = 'Somehow you get away.'
        else:
            health -= 5
            msg = (str("The %s hits you as \nyou're getting away"
                     ) % self.mob_stat[0])
            self.main_label.text = msg
            self.health_relative.remove_widget(self.health)
            self.remove_widget(self.health_relative)
            self.health = HealthBar(
                size_hint=(None, None),
                width=Window.width/2,
                height=Window.height/10
            )
            self.health_relative.add_widget(self.health)
            self.add_widget(self.health_relative)

        if health <= 0:
            global death_message
            if self.mob_stat[0] == 'creeper':
                death_message = ('You were blown to bits...')
            elif self.mob_stat[0] == 'witch':
                death_message = ("Well you married her.")
            elif self.mob_stat[0] == 'zombie':
                death_message = ("At least your\nbath has bubbles!")
            elif self.mob_stat[0] == 'skeleton':
                death_message = ("Even a bonehead\ncan kill you!")
            elif self.mob_stat[0] == 'spider':
                death_message = ("No you can't shoot webs,\n you're dead.")
            elif self.mob_stat[0] == 'slime':
                death_message = ("Oiled up, sexy, and ... dead.")
            engine.dead()
        else:
            self.minebtn.unbind(on_press=self.attack)
            self.remove_widget(self.minebtn)
            self.remove_widget(self.runbtn)
            self.add_widget(self.climbbtn)
            self.add_widget(self.deepbtn)

    def deep_callback(self, event):
        self.have_torch = False
        for i in inventory:
            if i[0] == 'torch' and i[1] > 0:
                self.have_torch = True
        if self.have_torch:
            engine.tick(1)
            engine.store('torch', -1)
            self.climbbtn.text = 'Climb Up'
            self.deep_cave(event)
        else:
            self.main_label.text = "You don't have any torches!"

    def climb_out(self, event):
        global main_text
        if self.climbbtn.text == 'Turn back':
            main_text = 'Good choice'
            sm.switch_to(Adventure())
        else:
            if random.randint(self.var_height, 70) < 60:
                engine.tick(1)
                search_mob = ['zombie', 'creeper', 'skeleton']
                mob = str(search_mob[random.randint(0, 2)])
                self.main_label.text = "A %s is engaging you\n" % mob
                self.minebtn.unbind(on_press=self.mine_ore)
                self.remove_widget(self.minebtn)
                self.minebtn.text = 'Attack'
                self.minebtn.bind(on_press=self.attack)
                self.minebtn.mob = mob
                self.add_widget(self.minebtn)
                self.var_height += 10
                self.fight(mob)
            else:
                sm.switch_to(Adventure())

    def cave_ore(self, height):
        global cave_ores
        mineable = []
        for i in cave_ores:
            if i[1] >= self.var_height:
                mineable.append(i[0])
        if self.var_height < 61:
            return str(mineable[random.randint(0, (len(mineable)-1))])
        else:
            return 'dirt'

    def deep_cave(self, event):
        self.climbbtn.text = 'Climb Up'
        global health
        global current_pickaxe
        height = self.var_height
        engine.tick(1)
        z = 0
        have_torch = False
        search = ['ore', 'monster']
        search_mob = ['zombie', 'creeper', 'skeleton']
        msg = ''
        # msg += health_bar()
        find = search[random.randint(0, 1)]
        if find == 'monster':
            mob = str(search_mob[random.randint(0, 2)])
            self.minebtn.unbind(on_press=self.mine_ore)
            self.remove_widget(self.minebtn)
            self.minebtn.text = 'Attack'
            self.minebtn.bind(on_press=self.attack)
            self.minebtn.mob = mob
            self.add_widget(self.minebtn)
            self.main_label.text = str(
                "There's a %s" % mob)
            self.var_height -= 10
            self.fight(mob)
        else:  # ore
            ore = self.cave_ore(height)
            self.minebtn.unbind(on_press=self.attack)
            self.remove_widget(self.minebtn)
            self.minebtn.text = 'Mine'
            self.minebtn.bind(on_press=self.mine_ore)
            self.ore = ore
            self.add_widget(self.minebtn)
            ore = ore.replace('_', ' ')
            self.main_label.text = str(
                '       You see some\n%s in the torchlight' % ore)
            self.var_height -= 10

    def fight(self, mob):
        global health
        self.remove_widget(self.climbbtn)
        self.remove_widget(self.deepbtn)
        self.add_widget(self.runbtn)
        # health bar
        if mob == 'zombie':
            zombie = Zombie()
            self.mob_stat = zombie.stats()

        elif mob == 'skeleton':
            skeleton = Skeleton()
            self.mob_stat = skeleton.stats()

        elif mob == 'creeper':
            creeper = Creeper()
            self.mob_stat = creeper.stats()

    # [0name, 1health, 2msg, 3drop, 4extra_drop]
    def attack(self, event):
        global death_message
        global health
        global current_sword
        self.blown_up = False
        if random.randint(0, 100) < 25:
            if self.mob_stat[0] == 'creeper':
                self.main_label.text = self.mob_stat[2]
                self.blown_up = True
                hurt = random.randint(60, 90)
                hurt = player.defense(hurt)
                health -= hurt
                
            else:
                hurt = random.randint(1, 4)
                if self.mob_stat[0] == 'witch':
                    hurt = random.randint(3, 8)
                hurt = player.defense(hurt)
                health -= hurt
                self.main_label.text = self.mob_stat[2]

        elif self.mob_stat[0] == 'witch' and random.randint(0, 100) < 10:
            self.main_label.text = 'The Witch heals itself\nwith a potion'
            self.mob_stat[1] += (random.randint(2, 8))

        else:
            if random.randint(0, 100) < 90:
                damage2 = player.damage()
                self.mob_stat[1] -= damage2
                self.main_label.text=str(
                    "You hit the %s for %s hp\n"
                    ) % (self.mob_stat[0], damage2)
            else:
                self.main_label.text=("You miss\n")
        self.health_relative.remove_widget(self.health)
        self.remove_widget(self.health_relative)
        self.health = HealthBar(
            size_hint=(None, None),
            width=Window.width/2,
            height=Window.height/10
        )
        self.health_relative.add_widget(self.health)
        self.add_widget(self.health_relative)
        # DEATH
        if health <= 0:
            global death_message
            if self.mob_stat[0] == 'creeper':
                death_message = ('You were blown to bits...')
            elif self.mob_stat[0] == 'witch':
                death_message = ("Well you married her.")
            elif self.mob_stat[0] == 'zombie':
                death_message = ("At least your\nbath has bubbles!")
            elif self.mob_stat[0] == 'skeleton':
                death_message = ("Even a bonehead\ncan kill you!")
            elif self.mob_stat[0] == 'spider':
                death_message = ("No you can't shoot webs,\n you're dead.")
            elif self.mob_stat[0] == 'slime':
                death_message = ("Oiled up, sexy, and ... dead.")
            engine.dead()

        if self.mob_stat[1] <= 0 and not self.blown_up:
            msg = ''
            msg += str("The %s has fallen\nby your %s\n"
                  ) % (self.mob_stat[0], current_sword[0])
            amount = random.randint(0, 3)
            if self.mob_stat[0] == 'witch':
                amount = random.randint(1, 2)
                drop = witch_drops[random.randint(0, len(witch_drops)-1)]
                engine.store(drop, amount)
                msg += str("You get %s %s!\n"
                  ) % (amount, drop)
            else:
                msg += str("You get %s %s!\n"
                  ) % (amount, self.mob_stat[3])
                engine.store(self.mob_stat[3], amount)
            stat.animal(self.mob_stat[0], 1)
            self.main_label.text = msg
            self.remove_widget(self.minebtn)
            self.remove_widget(self.runbtn)
            self.add_widget(self.climbbtn)
            self.add_widget(self.deepbtn)
        elif self.blown_up:
            stat.misc("creepers exploded", 1)
            self.main_label.text = 'The creeper blows up,\n hurting you badly'
            self.remove_widget(self.minebtn)
            self.remove_widget(self.runbtn)
            self.add_widget(self.climbbtn)
            self.add_widget(self.deepbtn)

    def mine_ore(self, event):
        # event.ore
        global current_pickaxe
        self.del_menu_buttons
        mine_time = (.5 / current_pickaxe[4])
        self.main_label.text = "You mine the %s" % self.ore
        if self.looping:
            self.del_menu_buttons()
            Clock.schedule_once(self.inter_label, mine_time * 1)
            Clock.schedule_once(self.inter_label, mine_time * 2)
            Clock.schedule_once(self.inter_label, mine_time * 3)
            Clock.schedule_once(self.finish_loop, mine_time * 3.1)
            Clock.schedule_once(self.mine_ore, mine_time * 3.5)
            Clock.schedule_once(self.add_menu_buttons, mine_time * 3.6)
            Clock.schedule_once(self.start_loop, mine_time * 5)
            engine.store(self.ore, 1)
            stat.ore(self.ore, 1)
        else:
            self.main_label.text = "Go Deeper?"

    def finish_loop(self, event):
        self.looping = False

    def start_loop(self, event):
        self.looping = True

    def del_menu_buttons(self):
        self.remove_widget(self.minebtn)
        self.remove_widget(self.climbbtn)
        self.remove_widget(self.deepbtn)

    def add_menu_buttons(self, *args):
        self.add_widget(self.climbbtn)
        self.add_widget(self.deepbtn)

    def inter_label(self, *args):
        self.main_label.text += '.'

    def pickaxe(self, block):
        global current_pickaxe
        global health
        new_text = ''
        if self.can_harvest(block):
            # input(msg, [3, float(.5/current_pickaxe[4])])
            if current_pickaxe[1] > 0 and current_pickaxe[0] != 'fist':
                    current_pickaxe[1] -= 1
            if current_pickaxe[1] == 0:
                alert("Your pickaxe has broken!")
                current_pickaxe = ['fist', -1, 0, -1, .5]
            new_text += str("You get 1 %s" % block.replace('_', ' '))
            self.label.text=new_text
            engine.store(block, 1)
            stat.ore(block, 1)
        else:
            if block == 'obsidian':
                new_text += "You use your water bucket to\n"
                new_text += "turn the lava into obsidian\n"
                new_text += "Your pickaxe isn't strong enough"
            else:
                new_text += "Your pickaxe isn't strong enough"
            self.main_label.text=new_text

    def can_harvest(self, block):

        # current_pickaxe = ['wooden_pickaxe', 33, 1, 59]
        can_mine = False
        for i in ores:
            if i[0] == block and i[2] <= current_pickaxe[2]:
                can_mine = True

        if can_mine:
            return True
        else:
            return False


class Adventure(Screen):  # animate

    def __init__(self, **kwargs):
        super(Adventure, self).__init__(**kwargs)
        # health bar
        self.bind(on_enter=self.starting)
        self.filled_bucket = False
        self.health = HealthBar(
            size_hint=(None, None),
            width=Window.width/2,
            height=Window.height/10
        )
        self.health_relative = RelativeLayout(
            size_hint=(None, None),
            pos_hint={'center_x': .33, 'center_y': .9}
        )
        self.health_relative.add_widget(self.health)
        self.add_widget(self.health_relative)
        # health bar
        self.selected_mob = None
        self.tree_chopped = False
        self.text = ''
        self.main_label = Label(
            size_hint=(None, None),
            font_size='40dp',
            width=int(Window.width)/4.0,
            height=int(Window.height)/4.0,
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.add_widget(self.main_label)

        self.btn1 = Button(
            text='Go Home',
            font_size='40dp',
            size_hint=(None, None),
            width=int(Window.width)/3,
            height=int(Window.height)/7.5,
            pos_hint={'right': .9, 'center_y': .05}

        )
        self.btn1.bind(on_press=self.go_home)
        self.add_widget(self.btn1)

        self.btn2 = Button(
            text='Adventure',
            font_size='40dp',
            size_hint=(None, None),
            width=int(Window.width)/3,
            height=int(Window.height)/7.5,
            pos_hint={'right': .4, 'center_y': .05}

        )
        self.btn2.bind(on_press=self.adv)
        self.add_widget(self.btn2)

        self.treebtn = Button(
            text='Break Tree',
            font_size='60dp',
            size_hint=(None, None),
            width=int(Window.width)/1.2,
            height=int(Window.height)/7.0,
            pos_hint={'center_x': .5, 'center_y': .3}
        )
        self.treebtn.bind(on_press=self.break_tree)

        self.fishbtn = Button(
            text='Fish',
            disabled=True,
            font_size='50dp',
            size_hint=(None, None),
            width=int(Window.width)/3.5,
            height=int(Window.height)/7.5,
            pos_hint={'right': .9, 'center_y': .25}

        )
        self.fishbtn.bind(on_press=self.fish)

        self.sandbtn = Button(
            text='Dig sand',
            font_size='50dp',
            size_hint=(None, None),
            width=int(Window.width)/3.5,
            height=int(Window.height)/7.5,
            pos_hint={'center_x': .8, 'center_y': .7}
        )
        self.sandbtn.bind(on_press=self.sand)

        self.bucketbtn = Button(
            text='Fill Bucket',
            disabled=True,
            font_size='50dp',
            size_hint=(None, None),
            width=int(Window.width)/3,
            height=int(Window.height)/7.5,
            pos_hint={'right': .4, 'center_y': .25}

        )
        self.bucketbtn.bind(on_press=self.fill_bucket)

        self.killbtn = Button(
            text='Attack',
            font_size='60dp',
            size_hint=(None, None),
            width=int(Window.width)/1.2,
            height=int(Window.height)/7.0,
            pos_hint={'center_x': .5, 'center_y': .3}
        )
        self.killbtn.bind(on_press=self.kill_mob)

        self.tamebtn = Button(
            text='Give Bone',
            font_size='60dp',
            size_hint=(None, None),
            width=int(Window.width)/1.2,
            height=int(Window.height)/7.0,
            pos_hint={'center_x': .5, 'center_y': .3}
        )
        self.tamebtn.bind(on_press=self.tame)

        self.runbtn = Button(
            text='Run Away',
            font_size='50dp',
            size_hint=(None, None),
            width=int(Window.width)/3.5,
            height=int(Window.height)/7.5,
            pos_hint={'right': .9, 'center_y': .05}
        )

        self.atkbtn = Button(
            text='Attack',
            font_size='60dp',
            size_hint=(None, None),
            width=int(Window.width)/1.2,
            height=int(Window.height)/7.0,
            pos_hint={'center_x': .5, 'center_y': .3}
        )

    def starting(self, event):
        self.main_label.text = self.adventure_text()

    def sand(self, event):
        global current_shovel
        self.bucketbtn.disabled = True
        self.fishbtn.disabled = True
        self.sandbtn.disabled = True
        self.btn1.disabled = True
        self.btn2.disabled = True
        var = float(.5/current_shovel[4])
        self.main_label.text = 'You fill your abnormally\nlarge pockets with sand'
        Clock.schedule_once(self.inter_label, 1 * var)
        Clock.schedule_once(self.inter_label, 2 * var)
        Clock.schedule_once(self.inter_label, 3 * var)
        Clock.schedule_once(self.river2, 3.2 * var)
        Clock.schedule_once(self.sand_dug, 3.1 * var)
        engine.store('sand', 1)

    def shovel(self, block):
        global current_shovel

        # input(msg, [3, float(.5/current_shovel[4])])
        if current_shovel[1] > 0 and current_shovel[0] != 'fist':
                current_shovel[1] -= 1

        if current_shovel[1] == 0:
            alert("Your shovel has broken...")
            current_shovel = ['fist', -1, 0, -1, .5]

    def inter_label(self, *args):
        self.main_label.text += '.'

    def sand_dug(self, dt):
        self.main_label.text = 'You get one sand!'
        self.sandbtn.disabled = False
        self.btn1.disabled = False
        self.btn2.disabled = False

    # zombie = Zombie()
    # [0health, 1msg, 2drop, 3extra_drop]
    # print(zombie.stats())

    def fight(self, mob):
        global health
        self.remove_widget(self.btn1)
        self.remove_widget(self.btn2)
        # health bar
        if mob == 'zombie':
            zombie = Zombie()
            self.mob_stat = zombie.stats()
            self.runbtn.bind(on_press=self.run)
            self.atkbtn.bind(on_press=self.attack)
            self.add_widget(self.runbtn)
            self.add_widget(self.atkbtn)

        elif mob == 'skeleton':
            skeleton = Skeleton()
            self.mob_stat = skeleton.stats()
            self.runbtn.bind(on_press=self.run)
            self.atkbtn.bind(on_press=self.attack)
            self.add_widget(self.runbtn)
            self.add_widget(self.atkbtn)

        elif mob == 'witch':
            witch = Witch()
            self.mob_stat = witch.stats()
            self.runbtn.bind(on_press=self.run)
            self.atkbtn.bind(on_press=self.attack)
            self.add_widget(self.runbtn)
            self.add_widget(self.atkbtn)

        elif mob == 'slime':
            slime = Slime()
            self.mob_stat = slime.stats()
            self.runbtn.bind(on_press=self.run)
            self.atkbtn.bind(on_press=self.attack)
            self.add_widget(self.runbtn)
            self.add_widget(self.atkbtn)

        elif mob == 'creeper':
            creeper = Creeper()
            self.mob_stat = creeper.stats()
            self.runbtn.bind(on_press=self.run)
            self.atkbtn.bind(on_press=self.attack)
            self.add_widget(self.runbtn)
            self.add_widget(self.atkbtn)

        else:
            spider = Spider()
            self.mob_stat = spider.stats()
            self.runbtn.bind(on_press=self.run)
            self.atkbtn.bind(on_press=self.attack)
            self.add_widget(self.runbtn)
            self.add_widget(self.atkbtn)

    # [0name, 1health, 2msg, 3drop, 4extra_drop]
    def attack(self, event):
        global health
        global current_sword
        global death_message
        self.blown_up = False
        if random.randint(0, 100) < 25:
            if self.mob_stat[0] == 'creeper':
                self.main_label.text = self.mob_stat[2]
                self.blown_up = True
                hurt = random.randint(60, 90)
                hurt = player.defense(hurt)
                health -= hurt
                
            else:
                hurt = random.randint(1, 4)
                if self.mob_stat[0] == 'witch':
                    hurt = random.randint(3, 8)
                hurt = player.defense(hurt)
                health -= hurt
                self.main_label.text = self.mob_stat[2]
        
        elif self.mob_stat[0] == 'witch' and random.randint(0, 100) < 30:
            self.main_label.text = 'The Witch heals itself\nwith a potion'
            self.mob_stat[1] += (random.randint(2, 10))

        else:
            if random.randint(0, 100) < 90:
                damage2 = player.damage()
                self.mob_stat[1] -= damage2
                self.main_label.text=str(
                    "You hit the %s for %s hp\n"
                    ) % (self.mob_stat[0], damage2)
            else:
                self.main_label.text=("You miss\n")
        self.health_relative.remove_widget(self.health)
        self.remove_widget(self.health_relative)
        self.health = HealthBar(
            size_hint=(None, None),
            width=Window.width/2,
            height=Window.height/10
        )
        self.health_relative.add_widget(self.health)
        self.add_widget(self.health_relative)
        # DEATH
        if health <= 0:
            global death_message
            if self.mob_stat[0] == 'creeper':
                death_message = ('You were blown to bits...')
            elif self.mob_stat[0] == 'witch':
                death_message = ("Well you married her.")
            elif self.mob_stat[0] == 'zombie':
                death_message = ("At least your\nbath has bubbles!")
            elif self.mob_stat[0] == 'skeleton':
                death_message = ("Even a bonehead\ncan kill you!")
            elif self.mob_stat[0] == 'spider':
                death_message = ("No you can't shoot webs,\n you're dead.")
            elif self.mob_stat[0] == 'slime':
                death_message = ("Oiled up, sexy, and ... dead.")
            engine.dead()

        if self.mob_stat[1] <= 0 and not self.blown_up:
            msg = ''
            msg += str("The %s has fallen\nby your %s\n"
                  ) % (self.mob_stat[0], current_sword[0])
            amount = random.randint(0, 3)
            if self.mob_stat[0] == 'witch':
                amount = random.randint(1, 2)
                drop = witch_drops[random.randint(0, len(witch_drops)-1)]
                engine.store(drop, amount)
                msg += str("You get %s %s!\n"
                  ) % (amount, drop)
            else:
                msg += str("You get %s %s!\n"
                  ) % (amount, self.mob_stat[3])
                engine.store(self.mob_stat[3], amount)
            stat.animal(self.mob_stat[0], 1)
            self.main_label.text = msg
            self.remove_widget(self.atkbtn)
            self.remove_widget(self.runbtn)
            self.add_widget(self.btn1)
            self.add_widget(self.btn2)
        elif self.blown_up:
            self.main_label.text = 'The creeper blows up,\n hurting you badly'
            stat.misc("creepers exploded", 1)
            self.remove_widget(self.atkbtn)
            self.remove_widget(self.runbtn)
            self.add_widget(self.btn1)
            self.add_widget(self.btn2)

    def run(self, event):
        global health
        if self.mob_stat[0] == 'creeper':
            self.main_label.text = 'Somehow you get away.'
        else:
            health -= 5
            self.health_relative.remove_widget(self.health)
            self.remove_widget(self.health_relative)
            self.health = HealthBar(
                size_hint=(None, None),
                width=Window.width/2,
                height=Window.height/10
            )
            self.health_relative.add_widget(self.health)
            self.add_widget(self.health_relative)
            msg = (str("The %s hits you as you're getting away"
                       ) % self.mob_stat[0])
            self.main_label.text = msg

        if health <= 0:
            global death_message
            if self.mob_stat[0] == 'creeper':
                death_message = ('You were blown to bits...')
            elif self.mob_stat[0] == 'witch':
                death_message = ("Well you married her.")
            elif self.mob_stat[0] == 'zombie':
                death_message = ("At least your\nbath has bubbles!")
            elif self.mob_stat[0] == 'skeleton':
                death_message = ("Even a bonehead\ncan kill you!")
            elif self.mob_stat[0] == 'spider':
                death_message = ("No you can't shoot webs,\n you're dead.")
            elif self.mob_stat[0] == 'slime':
                death_message = ("Oiled up, sexy, and ... dead.")
            engine.dead()
        else:
            self.remove_widget(self.atkbtn)
            self.remove_widget(self.runbtn)
            self.add_widget(self.btn1)
            self.add_widget(self.btn2)
            self.adv('')

    def adventure_text(self):
        global furnace_level
        if sc('tree', 'logs') < 50:
            text = ''
            text += "Chop down some trees and\n"
            text += "build some tools\n"
            text += "...\n"
        elif not sc('craft', 'furnace'):
            text = ''
            text += "Mine some stone and\n"
            text += "build a furnace\n"
            text += "...\n"
        elif sc('craft', 'bucket') < 4:
            text = ''
            text += "Cook some iron and\n"
            text += "build better tools\n"
            text += "...\n"
        elif furnace_level < 3:
            text = ''
            text += "Level up your furnace\n"
            text += "with some cobblestone\n"
            text += "...\n"
        elif sc('craft', 'torch') < 8:
            text = ''
            text += "Make some torches\n"
            text += "for cave diving\n"
            text += "...\n"
        elif sc('misc', 'wolf') < 3:
            text = ''
            text += "Tame some wolves\n"
            text += "to increase your damage\n"
            text += "...\n"
        elif not farming_started:
            text = ''
            text += "Build a farm\n"
            text += "...\n"
            text += "...\n"
        # elif sc('', '') < 50:
        #     text = ''
        #     text += "\n"
        #     text += "\n"
        #     text += "...\n"
        # elif sc('', '') < 50:
        #     text = ''
        #     text += "\n"
        #     text += "\n"
        #     text += "...\n"
        
        
        return text

    def adv(self, event):
        engine.tick(1)
        if self.treebtn:
            self.remove_widget(self.treebtn)
        if self.fishbtn:
            self.remove_widget(self.fishbtn)
        if self.bucketbtn:
            self.remove_widget(self.bucketbtn)
        if self.tamebtn:
            self.remove_widget(self.tamebtn)
        if self.killbtn:
            self.remove_widget(self.killbtn)
        if self.atkbtn:
            self.remove_widget(self.atkbtn)
        if self.runbtn:
            self.remove_widget(self.runbtn)
        if self.sandbtn:
            self.remove_widget(self.sandbtn)
        search = ['tree', 'tree', 'tree', 'tree',
                  'river', 'animal', 'animal', 'cave']
        if self.lapis_armor():
            if random.randint(0, 100) < 80:
                search.append('villager')
        else:
            if random.randint(0, 100) < 25:
                search.append('villager')
        end = search[random.randint(0, (len(search)-1))]
        if end == 'animal':
            self.mob()
        elif end == 'tree':
            self.add_widget(self.treebtn)
            self.main_label.text = 'Tree'
        elif end == 'river':
            self.river()
        elif end == 'cave':
            sm.switch_to(CaveScreen())
        elif end == 'villager':
            sm.switch_to(VillagerScreen())

    # Defines what mob you will find on an adventure
    def mob(self):

        global animal
        global animal_night
        global night
        engine.tick(1)
        mob_type = 0
        if night:
            mob_type = animal_night
            mob = mob_type[random.randint(0, (len(animal_night)-1))]
        else:
            mob_type = animal
            mob = mob_type[random.randint(0, (len(animal)-1))]
        self.selected_mob = mob
        self.fight_mob(mob)

    def fight_mob(self, mob):

        global health
        global friend
        global foe
        wolf = ['wolf']
        msg = ''

        if (mob) in friend:
            msg += "The %s won't stop following you!\n" % mob
            self.main_label.text = msg
            self.add_widget(self.killbtn)

        elif (mob) in wolf:
            msg += ("A wolf growls at you\n")
            for i in inventory:
                if i[0] == 'bone':
                    msg += ("Maybe you should give him a bone\n")
                    self.add_widget(self.tamebtn)
            self.main_label.text = msg

        else:
            self.main_label.text = "A %s is engaging you\n" % mob
            self.fight(mob)

    def tame(self, event):
        global wolves
        global damage
        engine.store('bone', -1)
        for i in inventory:
            if i[0] == 'bone':
                self.tamebtn.text = "Give Bone | %s" % i[1]
        if random.randint(0, 100) < 20:
            msg = "Tame successful!\n"
            msg += "Your damage increases by 1"
            self.main_label.text = msg
            self.remove_widget(self.tamebtn)
            stat.misc('wolf_tamed', 1)
            wolves += 1
        else:
            self.main_label.text = "Tame unsuccessful\n"
        for i in inventory:
            if i[0] == 'bone' and i[1] == 0 and self.tamebtn:
                self.remove_widget(self.tamebtn)

    def kill_mob(self, event):
        msg = ''
        mob = self.selected_mob
        if mob == 'sheep':
            amount = random.randint(0, 3)
            amount2 = random.randint(0, 3)
            engine.store('wool', amount)
            engine.store('raw_lambchop', amount2)
            msg += ("You get %s wool and %s raw lambchop!\n"
                    ) % (amount, amount2)
            self.main_label.text=msg
        elif mob == 'chicken':
            amount = random.randint(0, 3)
            amount2 = random.randint(0, 3)
            engine.store('feather', amount)
            engine.store('raw_chicken', amount2)
            msg += ("You get %s feathers and %s raw chicken!\n"
                    ) % (amount, amount2)
            self.main_label.text=msg
        elif mob == 'pig':
            amount = random.randint(0, 3)
            engine.store('raw_porkchop', amount)
            msg += ("You get %s raw porkchop!\n") % amount
            self.main_label.text=msg
        elif mob == 'cow':
            amount = random.randint(0, 3)
            amount2 = random.randint(0, 3)
            engine.store('raw_beef', amount)
            engine.store('leather', amount2)
            msg += ("You get %s raw beef, and %s leather!\n"
                    ) % (amount, amount2)
            self.main_label.text=msg
        stat.animal(mob, 1)

        self.remove_widget(self.killbtn)

    def fish(self, *args):
        self.bucketbtn.disabled = True
        self.fishbtn.disabled = True
        self.sandbtn.disabled = True
        self.btn1.disabled = True
        self.btn2.disabled = True
        self.main_label.text = 'You throw in your line'
        Clock.schedule_once(self.inter_label, .5)
        Clock.schedule_once(self.inter_label, 1)
        Clock.schedule_once(self.inter_label, 1.5)
        Clock.schedule_once(self.fish_label, 2)
        Clock.schedule_once(self.inter_label, 2.5)
        Clock.schedule_once(self.inter_label, 3)
        Clock.schedule_once(self.inter_label, 3.5)
        Clock.schedule_once(self.river2, 4)
        if random.randint(0, 100) < 30:
            stat.misc('fish_caught', 1)
            engine.store('raw_fish', 1)
            Clock.schedule_once(self.bite, 4)
        elif random.randint(0, 100) < 20:
            Clock.schedule_once(self.item_bite, 4)
        else:
            Clock.schedule_once(self.no_bite, 4)
    
    def fish_label(self, dt):
        self.main_label.text = 'You throw in your line'
    
    def item_bite(self, *args):
        global fishing_items
        item = fishing_items[random.randint(0, (
                             len(fishing_items)-1))]
        engine.store(item, 1)
        self.main_label.text="You caught a %s\n" % item

    def no_bite(self, *args):
        self.main_label.text="No bite, keep fishing?\n"

    def bite(self, *args):
        self.main_label.text="You caught a fish!\n"

    def fill_bucket(self, *args):
        self.main_label.text = 'Your bucket fills with water'
        for i in inventory:
                if i[0] == 'bucket' and i[1] >= 1:
                    engine.store('bucket', -1)
                    engine.store('water_bucket', 1)
                    stat.misc("bucket_filled", 1)
        self.filled_bucket = True
        Clock.schedule_once(self.river2)
        Clock.schedule_once(self.bucket_label, .1)

    def bucket_label(self, dt):
        self.main_label.text = "Don't spill it!"

    def river(self, *args):
        rod = False
        bucket = False
        msg = ''
        msg += ("You see a river!\n")
        for i in inventory:
            if i[0] == 'fishing_rod':
                rod = True

        for i in inventory:
            if i[0] == 'bucket' and i[1] > 0:
                if i[0] != 'water_bucket':
                    bucket = True
        self.remove_widget(self.bucketbtn)
        self.remove_widget(self.fishbtn)
        self.remove_widget(self.sandbtn)
        self.remove_widget(self.btn1)
        self.remove_widget(self.btn2)
        self.add_widget(self.bucketbtn)
        self.add_widget(self.fishbtn)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.sandbtn)
        if bucket and rod:
            if not self.filled_bucket:
                msg += "Would you like to fish or\n"
                msg += "fill your bucket with water?\n"
                self.main_label.text = msg
            self.fishbtn.disabled = False
            self.bucketbtn.disabled = False

        elif bucket:
            if not self.filled_bucket:
                msg += ("Would you like to fill a bucket with water?\n")
                self.main_label.text = msg
            self.bucketbtn.disabled = False

        elif rod:
            if not self.filled_bucket:
                msg += ("Would you like to fish?\n")
                self.main_label.text = msg
            self.fishbtn.disabled = False

        else:
            msg += ("Sorry there's nothing for you here.\n")
            self.main_label.text = msg

    def river2(self, *args):
        self.sandbtn.disabled = False
        self.btn1.disabled = False
        self.btn2.disabled = False
        rod = False
        bucket = False
        msg = ''
        msg += ("You see a river!\n")
        for i in inventory:
            if i[0] == 'fishing_rod':
                rod = True

        for i in inventory:
            if i[0] == 'bucket' and i[1] > 0:
                if i[0] != 'water_bucket':
                    bucket = True
        self.bucketbtn.disabled = True
        self.fishbtn.disabled = True
        if bucket and rod:
            if not self.filled_bucket:
                msg += "Would you like to fish or\n"
                msg += "fill your bucket with water?\n"
                self.main_label.text = msg
            self.fishbtn.disabled = False
            self.bucketbtn.disabled = False

        elif bucket:
            if not self.filled_bucket:
                msg += ("Would you like to fill a bucket with water?\n")
                self.main_label.text = msg
            self.bucketbtn.disabled = False

        elif rod:
            if not self.filled_bucket:
                msg += ("Would you like to fish?\n")
                self.main_label.text = msg
            self.fishbtn.disabled = False

        else:
            msg += ("Sorry there's nothing for you here.\n")
            self.main_label.text = msg

    def lapis_armor(self):
        global current_helmet
        global current_chestplate
        global current_leggings
        global current_boots

        if ('lapis' in current_helmet[0] and
            'lapis' in current_chestplate[0]and
            'lapis' in current_leggings[0] and
            'lapis' in current_boots[0]):
            return True

    def break_tree(self, event):
        global current_axe

        msg = ''
        z = 0
        logs = 0  # logs
        apples = 0  # apples
        amount3 = 0

        logs = random.randint(3, 7)
        if random.randint(0, 100) > 90 and current_axe[0] != 'fist':
            logs = random.randint(8, 16)
            apples = random.randint(2, 5)
            amount3 = logs
            msg += str(("You got %s logs!\n") % logs)
            stat.tree('big_trees', 1)
        elif random.randint(0, 100) < 30:
            apples = random.randint(1, 4)
            msg += str(("You got %s logs!\n") % logs)
            msg += str(("You got %s apples!\n") % apples)
            stat.tree('trees', 1)
        else:
            stat.tree('trees', 1)
            msg += str(("You got %s logs!\n") % logs)
            msg += ("Guess you're going to the doctor today!\n")

        msg2 = msg
        self.interval('You break a log',
                          True, logs, apples, logs, msg2)
        self.treebtn.disabled = True

    # input(msg, [3, float(.5/current_shovel[4])])
    def interval(self, msg, firsttime, logs, apples, iterations, msg2, *args):
        global current_axe
        timex = .5/current_axe[4]
        if iterations > 0 and firsttime:
            self.btn2.unbind(on_press=self.adv)
            self.total_logs = logs
            iterations = 3 * logs
            iterations -= 1
            msg = str(msg) + '.'
            self.main_label.text=msg
            Clock.schedule_once(partial(self.interval,
                    msg, False, logs, apples, iterations, msg2), timex)
        elif iterations > 0:
            iterations -= 1
            if len(msg) == 18:
                msg = 'You break a log'
            if current_axe[1] > 0 and current_axe[0] != 'fist':
                current_axe[1] -= 1

            if current_axe[1] == 0:
                alert("Your axe has broken!")
                current_axe = ['fist', -1, 0, -1, .5]
            msg = str(msg) + '.'
            self.main_label.text=msg
            Clock.schedule_once(partial(self.interval,
                    msg, False, logs, apples, iterations, msg2), timex)
        else:
            self.btn2.bind(on_press=self.adv)
            self.treebtn.disabled = False
            self.remove_widget(self.treebtn)
            engine.store('log', logs)
            engine.store('apple', apples)
            self.main_label.text = msg2
            stat.tree('logs', logs)
            if apples > 0:
                stat.tree('apples', apples)

    def go_home(self, event):
        global main_text
        main_text = 'back from adventuring...'
        sm.switch_to(MainScreen())


class VillagerScreen(Screen):
    
    def __init__(self, **kwargs):
        super(VillagerScreen, self).__init__(**kwargs)
        self.bind(on_enter=self.start1)

        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .1, 'center_y': .92}
        )
        self.exitbtn.bind(on_press=self.exit_callback)
        self.add_widget(self.exitbtn)

        self.msg_label = Label(
            text='',
            font_size='30dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            pos_hint={'center_x': .65, 'center_y': .9}
        )
        self.add_widget(self.msg_label)

        self.money_label = Label(
            font_size='40dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            pos_hint={'center_x': .3, 'center_y': .9}
        )
        self.add_widget(self.money_label)

        self.sell_label = Label(
            font_size='33dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            pos_hint={'center_x': .7, 'center_y': .75}
        )
        self.add_widget(self.sell_label)

        self.buy_label = Label(
            font_size='33dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            pos_hint={'center_x': .3, 'center_y': .75}
        )
        self.add_widget(self.buy_label)

        self.sell1 = Button(
            text='sell 1',
            font_size='33dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/8,
            pos_hint={'center_x': .3, 'center_y': .6}
        )
        self.sell1.quantity = 1
        self.sell1.bind(on_press=self.sell_callback)

        self.sell5 = Button(
            text='sell 5',
            font_size='33dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/8,
            pos_hint={'center_x': .3, 'center_y': .45}
        )
        self.sell5.quantity = 5
        self.sell5.bind(on_press=self.sell_callback)

        self.sell10 = Button(
            text='sell 10',
            font_size='33dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/8,
            pos_hint={'center_x': .3, 'center_y': .30}
        )
        self.sell10.quantity = 10
        self.sell10.bind(on_press=self.sell_callback)

        self.sell_all = Button(
            text='sell all',
            font_size='33dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/8,
            pos_hint={'center_x': .3, 'center_y': .15}
        )
        self.sell_all.quantity = 10000
        self.sell_all.bind(on_press=self.sell_callback)

        self.buy1 = Button(
            text='buy 1',
            font_size='33dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/8,
            pos_hint={'center_x': .7, 'center_y': .6}
        )
        self.buy1.quantity = 1
        self.buy1.bind(on_press=self.buy_callback)

        self.buy5 = Button(
            text='buy 5',
            font_size='33dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/8,
            pos_hint={'center_x': .7, 'center_y': .45}
        )
        self.buy5.quantity = 5
        self.buy5.bind(on_press=self.buy_callback)

        self.buy10 = Button(
            text='buy 10',
            font_size='33dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/8,
            pos_hint={'center_x': .7, 'center_y': .30}
        )
        self.buy10.quantity = 10
        self.buy10.bind(on_press=self.buy_callback)

        self.buy_all = Button(
            text='buy all',
            font_size='33dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/8,
            pos_hint={'center_x': .7, 'center_y': .15}
        )
        self.buy_all.quantity = 10000
        self.buy_all.bind(on_press=self.buy_callback)

    def sell_callback(self, event):
        self.quantity = event.quantity
        sold_quantity = 0
        for i in inventory:
            if self.item_for_sale[0] == i[0]:
                material_quantity = i[1]
        for i in range(self.quantity):
            if material_quantity > 0:
                engine.store(self.item_for_sale[0], -1)
                engine.money_add(copy.deepcopy(self.item_for_sale[1])/2.0)
                material_quantity -= 1
                sold_quantity += 1
        self.msg_label.text = "You sold %s %s!" % (
            sold_quantity, self.item_for_sale[0]
        )
        self.starting()

    def buy_callback(self, event):
        self.quantity = event.quantity
        bought_quantity = 0
        for i in range (self.quantity):
            global money
            if money >= self.item_for_buy[1]:
                engine.store(self.item_for_buy[0], 1)
                engine.money_add(-(self.item_for_buy[1]))
                bought_quantity += 1
        self.msg_label.text = "You bought %s %s!" % (
            bought_quantity, self.item_for_buy[0]
        )
        self.starting()

    def exit_callback(self, event):
        sm.switch_to(Adventure())

    def start1(self, event):
        self.define_items()
        self.starting()

    def define_items(self):
        global prices
        buying_selling = True
        self.item_for_sale = 0
        self.item_for_buy = 0
        self.quantity_buy = 0
        self.quantity_sell = 0
        select = 0
        z = 5
        sell_list = copy.deepcopy(prices)
        buy_list = prices
        for i in inventory:
            for x in prices:
                if i[0] == x[0]:
                    sell_list.append(x)
                    if z != 0:
                        sell_list.remove(sell_list[(z - 1)])
                        z -= 1
        # ['leather', 5]
        self.item_for_sale = sell_list[random.randint(0,
                                      (len(sell_list)-1))]
        sell_list.remove(self.item_for_sale)
        self.item_for_buy = buy_list[random.randint(0,
                                    (len(buy_list)-1))]
        self.sell_label.text = 'Villager is selling\n%s for $%s' % (
            self.item_for_buy[0], float(self.item_for_buy[1])
        )
        self.buy_label.text = 'Villager is buying\n%s for $%s' % (
            self.item_for_sale[0], self.item_for_sale[1]/2.0
        )
        if self.item_for_sale[0] == self.item_for_buy[0]:
            self.define_items()

    def starting(self):
        self.money_label.text = '$%s' % money
        self.quantity_sell = 0
        self.quantity_buy = 0
        for i in inventory:
            if i[0] == self.item_for_sale[0] and i[1] > 0:
                have_item_sell = True
                self.quantity_sell = i[1]
        if money >= self.item_for_buy[1]:
            have_item_buy = True
            self.quantity_buy = math.floor(money/(self.item_for_buy[1]))
        self.remove_widget(self.buy1)
        self.remove_widget(self.buy5)
        self.remove_widget(self.buy10)
        self.remove_widget(self.buy_all)
        self.remove_widget(self.sell1)
        self.remove_widget(self.sell5)
        self.remove_widget(self.sell10)
        self.remove_widget(self.sell_all)
        if self.quantity_buy > 0:
            self.add_widget(self.buy1)
        if self.quantity_buy >= 5:
            self.add_widget(self.buy5)
        if self.quantity_buy >= 10:
            self.add_widget(self.buy10)
        if self.quantity_buy >= 11:
            self.add_widget(self.buy_all)
        if self.quantity_sell > 0:
            self.add_widget(self.sell1)
        if self.quantity_sell > 5:
            self.add_widget(self.sell5)
        if self.quantity_sell > 10:
            self.add_widget(self.sell10)
        if self.quantity_sell > 11:
            self.add_widget(self.sell_all)


class DigDownScreen(Screen):  # animate

    def __init__(self, **kwargs):
        super(DigDownScreen, self).__init__(**kwargs)
        global height
        self.water_buckets = 0
        for i in inventory:
            if i[0] == 'water_bucket' and i[1] > 0:
                self.water_buckets = i[1]
        height = 64
        # health bar
        self.health = HealthBar(
            size_hint=(None, None),
            width=Window.width/2,
            height=Window.height/10
        )
        self.health_relative = RelativeLayout(
            size_hint=(None, None),
            pos_hint={'center_x': .5, 'center_y': .1}
        )
        self.health_relative.add_widget(self.health)
        self.add_widget(self.health_relative)
        # health bar
        self.digbtn = Button(
            text="Dig Down",
            font_size='60dp',
            size_hint=(None, None),
            width=int(Window.width)/1.2,
            height=int(Window.height)/7.0,
            pos_hint={'center_x': .5, 'center_y': .25}
        )

        self.climbbtn = Button(
            text='Climb Out',
            font_size='50dp',
            size_hint=(None, None),
            width=int(Window.width)/3.5,
            height=int(Window.height)/7.5,
            pos_hint={'center_x': .2, 'center_y': .07}
        )

        self.label = Label(
            text="Don't fall in lava!",
            font_size='35dp',
            size_hint_y=None,
            height=int(Window.height),
            size_hint_x=None,
            width=int(Window.width),
            pos_hint={'center_x': .5, 'center_y': .6}
        )

        self.bucket_label = Label(
            font_size='25dp',
            size_hint=(None, None),
            width=int(Window.width)/3.5,
            height=int(Window.height)/7.5,
            pos_hint={'center_x': .5, 'center_y': .85}
        )
        self.add_widget(self.bucket_label)

        self.add_widget(self.climbbtn)
        self.add_widget(self.digbtn)
        self.add_widget(self.label)
        self.digbtn.bind(on_press=self.dig)
        self.climbbtn.bind(on_press=self.climb)

    def dig(self, event):
        global height
        engine.tick(1)
        block = self.ore(height)
        height -= 1

        if block != 'bedrock' and block != 'lava':
            self.bucket_label.text = '%s-water buckets' % self.water_buckets
            self.interval('You mine the block below you',
                          True, block, 3)

        elif block == 'bedrock':
            self.label.text = "You can't mine through bedrock!"
            self.digbtn.disabled = True
        else:
            if self.water_buckets > 0:
                self.interval('You mine the block below you',
                              True, block, 3)
                self.lava_bucket()
            else:
                self.lava_no_bucket()

    def shovel(self, block):
        global current_shovel

        # input(msg, [3, float(.5/current_shovel[4])])
        if current_shovel[1] > 0 and current_shovel[0] != 'fist':
                current_shovel[1] -= 1

        if current_shovel[1] == 0:
            alert("Your shovel has broken...")
            current_shovel = ['fist', -1, 0, -1, .5]

        self.label.text="You get 1 %s" % block.replace('_', ' ').replace('_', ' ')
        engine.store(block, 1)
        stat.ore(block, 1)

    def pickaxe(self, block):
        global current_pickaxe
        new_text = ''
        if self.can_harvest(block):
            # input(msg, [3, float(.5/current_pickaxe[4])])
            if current_pickaxe[1] > 0 and current_pickaxe[0] != 'fist':
                    current_pickaxe[1] -= 1

            if current_pickaxe[1] == 0:
                alert("Your pickaxe has broken...")
                current_pickaxe = ['fist', -1, 0, -1, .5]

            if block == 'obsidian':
                new_text += "You use your water bucket to\n"
                new_text += "turn the lava into obsidian\n"
                new_text += "barely singeing your feet\n"
                new_text += str("You get 1 %s" % block.replace('_', ' '))
            else:
                new_text += str("You get 1 %s" % block.replace('_', ' '))

            self.label.text=new_text
            engine.store(block, 1)
            stat.ore(block, 1)
        else:
            if block == 'obsidian':
                new_text += "You use your water bucket to\n"
                new_text += "turn the lava into obsidian\n"
                new_text += "barely singeing your feet\n"
                new_text += "Your pickaxe isn't strong enough"
            else:
                new_text += "Your pickaxe isn't strong enough"
            self.label.text=new_text

    def lava_bucket(self):
        global health
        health -= 10

        # update health bar
        self.health_relative.remove_widget(self.health)
        self.remove_widget(self.health_relative)
        self.health = HealthBar(
            size_hint=(None, None),
            width=Window.width/2,
            height=Window.height/10
        )
        self.health_relative.add_widget(self.health)
        self.add_widget(self.health_relative)
        stat.misc('lava_blocked', 1)
        engine.store('water_bucket', -1)
        self.water_buckets -= 1
        self.bucket_label.text = '%s-water buckets' % self.water_buckets
        engine.store('bucket', 1)

    def lava_no_bucket(self):
        global death_message
        death_message = "OUCH LAVA BURNS!"
        engine.dead()

    def climb(self, event):
        global main_text
        main_text = 'Back from digging...'
        sm.switch_to(MainScreen())

    # Calculates the ore found at x height
    def ore(self, height):

        # Takes current height and returns the available ores
        mineable = []

        for i in ores:
            if i[1] >= height:
                mineable.append(i[0])

        if height < 61:
            return mineable[random.randint(0, (len(mineable)-1))]
        else:
            return 'dirt'

        # Calculates if your current_pickaxe can break a block or not

    def can_harvest(self, block):

        # current_pickaxe = ['wooden_pickaxe', 33, 1, 59]
        can_mine = False
        for i in ores:
            if i[0] == block and i[2] <= current_pickaxe[2]:
                can_mine = True

        if not can_mine:
            return False
        else:
            return True

    # input(msg, [3, float(.5/current_shovel[4])])
    def interval(self, msg, firsttime, block, iterations, *args):
        global current_shovel
        global current_pickaxe
        global sm
        if block == 'dirt' or block =='gravel':
            timex = .5/current_shovel[4]
        elif block != 'lava':
            timex = .5/current_pickaxe[4]
        else:
            timex = .5/current_pickaxe[4]
            block = 'obsidian'
        if iterations > 0 and firsttime:
            iterations -= 1
            msg = str(msg) + '.'
            self.label.text=msg
            Clock.schedule_once(partial(self.interval,
                    msg, False, block, iterations), timex)
            self.digbtn.disabled = True
        elif iterations > 0:
            iterations -= 1
            msg = str(msg) + '.'
            self.label.text=msg
            Clock.schedule_once(partial(self.interval,
                    msg, False, block, iterations), timex)
        else:
            self.digbtn.disabled = False
            if block == 'dirt' or block =='gravel':
                self.shovel(block)
            elif block == 'lava':
                self.pickaxe('obsidian')
            else:
                self.pickaxe(block)


class Craft(Screen):  # animate
    def __init__(self, **kwargs):
        super(Craft, self).__init__(**kwargs)
        # armor_type
        # tool_type
        # block_type
        # misc_type
        self.block_scroll = ScrollView()
        self.block_grid = GridLayout()
        #self.bind(on_enter=self.starting)

    #def starting(self, event):
        self.table = False
        self.available = []
        self.selected_event = None
        self.selected_item = None
        self.selected_quantity = None
        self.added = 0
        crafting.sort()
        for i in inventory:
            if i[0] == 'crafting_table' and i[1] >= 1:
                self.table = True
        for i in crafting:
            if len(i) == 4:
                for x in inventory:
                    if i[1] == x[0] and i[2] <= x[1]:
                        self.available.append(i)
            elif self.table:
                for x in inventory:
                    if i[1] == x[0] and i[2] <= x[1]:
                        for z in inventory:
                            if i[3] == z[0] and i[4] <= z[1]:
                                self.available.append(i)

        self.scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height),
            pos_hint={'center_x': .5},
            bar_color=([.81, .55, .55, 1]),
            bar_inactive_color=([.55, .17, .17, 1]))
        
        self.scroll.scroll_y = Craft.scroll_pos

        self.grid = GridLayout(
            size_hint=(None, 2),
            cols=2
        )
        # building button grid
        for i in self.available:
            self.added += 1
            bstext = i[0]
            bstext = bstext.replace("_", " ")
            self.btn = Button(
                text=bstext,
                font_size='40dp',
                #item=i[0],
                size_hint=(.4, .4)
                #height=Window.height/4.0,
                #width=Window.width/2.22
            )
            self.btn.bind(on_press=self.callback)
            self.btn.item = i
            if len(i) == 6:
                self.btn.quantity = i[5]
            else:
                self.btn.quantity = i[3]
            self.grid.add_widget(self.btn)

        if self.added%2 == 1:
            self.btn = Button(
                text='',
                size_hint=(.4, .4),
                background_color=(0, 0, 0, 1)
            )
            self.grid.add_widget(self.btn)

        for i in range(6):
            self.btn = Button(
                text='',
                size_hint_x=None,
                # height=self.minimum_height,
                width=Window.width/2.22,
                background_color=(0, 0, 0, 1)
            )
            self.grid.add_widget(self.btn)

        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)

        self.craftbtn = Button(
            text='Craft',
            font_size='50dp',
            color = (0, 0, 0, 1),
            size_hint=(None, None),
            height=int(Window.height)/6,
            width=int(Window.width)/2,
            pos_hint={'center_x': .50}
        )
        self.add_widget(self.craftbtn)

        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit_craft)
        self.add_widget(self.exitbtn)

        self.btn1 = Button(
            text='+ 1',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .1, 'center_y': .3}
        )
        self.btn1.bind(on_press=self.add_button)

        self.btn5 = Button(
            text='+ 5',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .1, 'center_y': .1}
        )
        self.btn5.bind(on_press=self.add_button)

        self.btn10 = Button(
            text='+ 10',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .3}
        )
        self.btn10.bind(on_press=self.add_button)

        dropdown = DropDown()

        btn1 = Button(text='armor',
                      size_hint_y=None,
                      height=int(Window.height)/9,
                      background_color=(0.07, 0.26, 0.56, 1),
                      font_size='45dp')
        btn1.bind(on_release=lambda btn: dropdown.select(btn1.text))
        btn1.bind(on_press=self.type_select)
        dropdown.add_widget(btn1)

        btn2 = Button(text='tool',
                      size_hint_y=None,
                      height=int(Window.height)/9,
                      background_color=(0.07, 0.26, 0.56, 1),
                      font_size='45dp')
        btn2.bind(on_release=lambda btn: dropdown.select(btn2.text))
        btn2.bind(on_press=self.type_select)
        dropdown.add_widget(btn2)

        btn3 = Button(text='block',
                      size_hint_y=None,
                      height=int(Window.height)/9,
                      background_color=(0.07, 0.26, 0.56, 1),
                      font_size='45dp')
        btn3.bind(on_release=lambda btn: dropdown.select(btn3.text))
        btn3.bind(on_press=self.type_select)
        dropdown.add_widget(btn3)

        btn4 = Button(text='misc',
                      size_hint_y=None,
                      height=int(Window.height)/9,
                      background_color=(0.07, 0.26, 0.56, 1),
                      font_size='45dp')
        btn4.bind(on_release=lambda btn: dropdown.select(btn4.text))
        btn4.bind(on_press=self.type_select)
        dropdown.add_widget(btn4)


        self.mainbutton = Button(
                text='Type',
                font_size='45dp',
                size_hint=(None, None),
                width=int(Window.width)/4,
                height=int(Window.height)/6,
                size_hint_x=None,
                background_color=(0.07, 0.26, 0.56, 1),
                pos_hint={'center_x': .1, 'center_y': .1})
        self.mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))

        self.add_widget(self.mainbutton)

        if Craft.menu != 'main':
            if Craft.menu == 'armor':
                self.type_select2('armor')
            elif Craft.menu == 'tool':
                self.type_select2('tool')
            elif Craft.menu == 'block':
                self.type_select2('block')
            elif Craft.menu == 'misc':
                self.type_select2('misc')

    def build_armor(self):
        self.block_scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height),
            pos_hint={'center_x': .5},
            bar_color=([.81, .55, .55, 1]),
            bar_inactive_color=([.55, .17, .17, 1]))
        self.block_scroll.scroll_y = Craft.menu_scroll_pos
        self.block_grid = GridLayout(
            size_hint=(None, 2),
            cols=2
        )
        # building button grid
        for i in self.available:
            if i[0] in armor_type:
                self.added += 1
                bstext = i[0]
                bstext = bstext.replace("_", " ")
                self.btn = Button(
                    text=bstext,
                    font_size='40dp',
                    item=i[0],
                    size_hint_x=None,
                    height=Window.height/4.0,
                    width=Window.width/2.22
                )
                self.btn.bind(on_press=self.callback)
                self.btn.item = i
                if len(i) == 6:
                    self.btn.quantity = i[5]
                else:
                    self.btn.quantity = i[3]
                self.block_grid.add_widget(self.btn)
        if self.added%2 == 1:
            self.btn = Button(
                text='',
                size_hint_x=None,
                # height=self.minimum_height,
                width=Window.width/2.22,
                background_color=(0, 0, 0, 1)
            )
            self.block_grid.add_widget(self.btn)

        for i in range(6):
            self.btn = Button(
                text='',
                size_hint_x=None,
                # height=self.minimum_height,
                width=Window.width/2.22,
                background_color=(0, 0, 0, 1)
            )
            self.block_grid.add_widget(self.btn)
        self.block_scroll.add_widget(self.block_grid)

    def build_tool(self):
        self.block_scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height),
            pos_hint={'center_x': .5},
            bar_color=([.81, .55, .55, 1]),
            bar_inactive_color=([.55, .17, .17, 1]))
        self.block_scroll.scroll_y = Craft.menu_scroll_pos
        self.block_grid = GridLayout(
            size_hint=(None, 2),
            cols=2
        )
        # building button grid
        for i in self.available:
            if i[0] in tool_type:
                self.added += 1
                bstext = i[0]
                bstext = bstext.replace("_", " ")
                self.btn = Button(
                    text=bstext,
                    font_size='40dp',
                    item=i[0],
                    size_hint_x=None,
                    height=Window.height/4.0,
                    width=Window.width/2.22
                )
                self.btn.bind(on_press=self.callback)
                self.btn.item = i
                if len(i) == 6:
                    self.btn.quantity = i[5]
                else:
                    self.btn.quantity = i[3]
                self.block_grid.add_widget(self.btn)
        if self.added%2 == 1:
            self.btn = Button(
                text='',
                size_hint_x=None,
                # height=self.minimum_height,
                width=Window.width/2.22,
                background_color=(0, 0, 0, 1)
            )
            self.block_grid.add_widget(self.btn)

        for i in range(6):
            self.btn = Button(
                text='',
                size_hint_x=None,
                # height=self.minimum_height,
                width=Window.width/2.22,
                background_color=(0, 0, 0, 1)
            )
            self.block_grid.add_widget(self.btn)
        self.block_scroll.add_widget(self.block_grid)

    def build_block(self):
        self.block_scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height),
            pos_hint={'center_x': .5},
            bar_color=([.81, .55, .55, 1]),
            bar_inactive_color=([.55, .17, .17, 1]))
        self.block_scroll.scroll_y = Craft.menu_scroll_pos
        self.block_grid = GridLayout(
            size_hint=(None, 2),
            cols=2
        )
        # building button grid
        for i in self.available:
            if i[0] in block_type:
                self.added += 1
                bstext = i[0]
                bstext = bstext.replace("_", " ")
                self.btn = Button(
                    text=bstext,
                    font_size='40dp',
                    item=i[0],
                    size_hint_x=None,
                    height=Window.height/4.0,
                    width=Window.width/2.22
                )
                self.btn.bind(on_press=self.callback)
                self.btn.item = i
                if len(i) == 6:
                    self.btn.quantity = i[5]
                else:
                    self.btn.quantity = i[3]
                self.block_grid.add_widget(self.btn)

        if self.added%2 == 1:
            self.btn = Button(
                text='',
                size_hint_x=None,
                # height=self.minimum_height,
                width=Window.width/2.22,
                background_color=(0, 0, 0, 1)
            )
            self.block_grid.add_widget(self.btn)

        for i in range(6):
            self.btn = Button(
                text='',
                size_hint_x=None,
                # height=self.minimum_height,
                width=Window.width/2.22,
                background_color=(0, 0, 0, 1)
            )
            self.block_grid.add_widget(self.btn)
        self.block_scroll.add_widget(self.block_grid)

    def build_misc(self):
        self.block_scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height),
            pos_hint={'center_x': .5},
            bar_color=([.81, .55, .55, 1]),
            bar_inactive_color=([.55, .17, .17, 1]))
        self.block_scroll.scroll_y = Craft.menu_scroll_pos
        self.block_grid = GridLayout(
            size_hint=(None, 2),
            cols=2
        )
        # building button grid
        for i in self.available:
            if i[0] in misc_type:
                self.added += 1
                bstext = i[0]
                bstext = bstext.replace("_", " ")
                self.btn = Button(
                    text=bstext,
                    font_size='40dp',
                    item=i[0],
                    size_hint_x=None,
                    height=Window.height/4.0,
                    width=Window.width/2.22
                )
                self.btn.bind(on_press=self.callback)
                self.btn.item = i
                if len(i) == 6:
                    self.btn.quantity = i[5]
                else:
                    self.btn.quantity = i[3]
                self.block_grid.add_widget(self.btn)

        if self.added%2 == 1:
            self.btn = Button(
                text='',
                size_hint_x=None,
                # height=self.minimum_height,
                width=Window.width/2.22,
                background_color=(0, 0, 0, 1)
            )
            self.block_grid.add_widget(self.btn)

        for i in range(6):
            self.btn = Button(
                text='',
                size_hint_x=None,
                # height=self.minimum_height,
                width=Window.width/2.22,
                background_color=(0, 0, 0, 1)
            )
            self.block_grid.add_widget(self.btn)
        self.block_scroll.add_widget(self.block_grid)

    def type_select(self, event):
        self.remove_widget(self.scroll)
        self.remove_widget(self.exitbtn)
        self.remove_widget(self.craftbtn)
        self.remove_widget(self.mainbutton)
        self.block_scroll.clear_widgets()
        self.block_grid.clear_widgets()
        x = event.text
        if x == 'misc':
            self.build_misc()
            Craft.menu = 'misc'
        elif x == 'tool':
            self.build_tool()
            Craft.menu = 'tool'
        elif x == 'armor':
            self.build_armor()
            Craft.menu = 'armor'
        elif x == 'block':
            self.build_block()
            Craft.menu = 'block'
        self.add_widget(self.block_scroll)
        self.add_widget(self.mainbutton)
        self.add_widget(self.exitbtn)
        self.add_widget(self.craftbtn)

    def type_select2(self, text):
        x = text
        self.remove_widget(self.scroll)
        self.remove_widget(self.exitbtn)
        self.remove_widget(self.craftbtn)
        self.remove_widget(self.mainbutton)
        self.block_scroll.clear_widgets()
        self.block_grid.clear_widgets()
        if x == 'misc':
            self.build_misc()
            Craft.menu = 'misc'
        elif x == 'tool':
            self.build_tool()
            Craft.menu = 'tool'
        elif x == 'armor':
            self.build_armor()
            Craft.menu = 'armor'
        elif x == 'block':
            self.build_block()
            Craft.menu = 'block'
        self.add_widget(self.block_scroll)
        self.add_widget(self.mainbutton)
        self.add_widget(self.exitbtn)
        self.add_widget(self.craftbtn)

    def exit_craft(self, event):
        global main_text
        main_text = 'back from crafting...'
        Craft.scroll_pos = 1
        Craft.menu = 'main'
        Craft.menu_scroll_pos = 1
        sm.switch_to(MainScreen())

    def craft(self, event):
        for e in crafting:
            if e[0] == self.selected_item[0]:
                if len(e) == 6:
                    quantity = self.selected_quantity / self.selected_item[5]
                    engine.store(e[0], (e[5] * quantity))
                    engine.store(e[1], (-e[2] * quantity))
                    engine.store(e[3], (-e[4] * quantity))
                    stat.craft(e[0], (e[5] * quantity))
                    Craft.scroll_pos = self.scroll.scroll_y
                    Craft.menu_scroll_pos = self.block_scroll.scroll_y
                    sm.switch_to(Craft())

                else:
                    quantity = self.selected_quantity / self.selected_item[3]
                    engine.store(e[0], (e[3] * quantity))
                    engine.store(e[1], (-e[2] * quantity))
                    stat.craft(e[0], (e[3] * quantity))
                    Craft.scroll_pos = self.scroll.scroll_y
                    Craft.menu_scroll_pos = self.block_scroll.scroll_y
                    sm.switch_to(Craft())

    def possible_quantity(self):
        for e in crafting:
            # e is  ['bed', 'wool', 3, 'wood_plank', 3, 1],
            # for 2 material recipies
            if len(e) == 6 and self.selected_item == e:
                for x in inventory:
                    if e[1] == x[0]:
                        # (Quantity I have on hand /
                        # Quantity needed for recipie)
                        # rounded down * total amount given at end
                        # [Total amount of item craftable]
                        var1 = math.floor(x[1] / e[2])

                for x in inventory:
                    if e[3] == x[0]:
                        var2 = math.floor(x[1] / e[4])

                if var1 > var2:
                    return var2 * e[5]
                else:
                    return var1 * e[5]

            # ['wood_plank', 'log', 1, 4],
            # for 1 material recipies
            elif self.selected_item == e:
                for x in inventory:
                    if e[1] == x[0]:
                        # Total amount of item craftable
                        var1 = math.floor(x[1] / e[2])
                        return var1 * e[3]

    def add_button(self, event):
        # loop here for event.quantity change all to 1
        # loop to... add max out of
        # check to make sure the quantity is possible
        for x in range(event.quantity):
            if len(self.selected_item) == 6:
                var = self.selected_item[5]
            else:
                var = self.selected_item[3]
            if (self.selected_quantity
                ) < (int(self.possible_quantity())):
                self.selected_quantity += var
                self.craftbtn.text=str(
                    'Craft - %s' % self.selected_quantity)
            else:
                pass

    def callback(self, event):
        self.craftbtn.unbind(on_press=self.craft)
        self.craftbtn.bind(on_press=self.craft)
        self.selected_item = event.item
        self.selected_quantity = event.quantity
        self.remove_widget(self.btn1)
        self.remove_widget(self.btn5)
        self.remove_widget(self.btn10)
        if (self.selected_quantity
            ) < (self.possible_quantity()):
            self.add_widget(self.btn1)
        if (5 + self.selected_quantity
            ) < (self.possible_quantity()):
            self.add_widget(self.btn5)
        if (10 + self.selected_quantity
            ) < (self.possible_quantity()):
            self.add_widget(self.btn10)
        self.btn1.quantity=1
        self.btn5.quantity=5
        self.btn10.quantity=10
        self.craftbtn.text = 'Craft - %s' %self.selected_quantity

        try:
            self.selected_event.background_color = (1, 1, 1, 1)
        except AttributeError:
            pass
        self.selected_event = event
        event.background_color=(1, 0, 1, 1)


class Furnace(Screen):  # animate
    def __init__(self, **kwargs):
        super(Furnace, self).__init__(**kwargs)
        global time_left_cooking
        global furnace_level
        self.is_cooking = False
        self.cost = (23 * furnace_level)
        self.selected_event = None
        self.selected_item = None
        self.selected_quantity = 1
        self.possible_quantity = 1
        self.fuel = None
        self.material = None
        self.fuel_quantity = None
        self.material_quantity = None
        self.added = 0
        self.bind(on_leave=self.leaving)
        self.bind(on_enter=self.starting)
        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit_screen)
        self.add_widget(self.exitbtn)

        self.time_label = Label(
            font_size='45dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0,
            pos_hint={'center_y': .93, 'center_x': .8}
        )
        self.add_widget(self.time_label)
        self.cookbtn = Button(
            font_size='65dp',
            size_hint=(None, None),
            height=int(Window.height)/7.0,
            width=int(Window.width)/2.0,
            pos_hint={'center_x': .5}
        )

        self.levelbtn = Button(
            text='Expand',
            font_size='65dp',
            size_hint=(None, None),
            disabled=True,
            height=int(Window.height)/7.0,
            width=int(Window.width)/2.2,
            pos_hint={'center_x': .5, 'center_y': .22}
        )
        self.levelbtn.bind(on_press=self.level_furnace)
        self.add_widget(self.levelbtn)

        for i in inventory:
            if i[0] == 'cobblestone' and i[1] >= self.cost:
                self.levelbtn.disabled = False

        self.levelqtn = Label(
            text='Level: %s' % furnace_level,
            font_size='45dp',
            size_hint=(None, None),
            height=int(Window.height)/7.0,
            width=int(Window.width)/1.7,
            pos_hint={'center_x': .5, 'center_y': .33}
        )

        if furnace_level > 1:
            self.add_widget(self.levelqtn)
        
        if time_left_cooking > 0:
            self.remove_widget(self.time_label)
            self.time_label.text = str("Time Left: " +str(time_left_cooking))
            self.add_widget(self.time_label)
            self.cookbtn.text = 'Cooking.'
            self.cookbtn.background_color = (1.66, 0.47, 0.47, 1)
        else:
            self.cookbtn.text = 'Cook'
            self.cookbtn.background_color = (1.81, 1.86, 2.26, 1)

        self.cookbtn.bind(on_press=self.add_material)
        self.add_widget(self.cookbtn)

        # building popup for adding stuff
        self.add_stuff = Popup(
            title='',
        )
        self.add_stuff.bind(on_dismiss=self.exiting_popup)

        self.selection_scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height),
            pos_hint={'center_x': .5},
            bar_color=([.81, .55, .55, 1]),  #
            bar_inactive_color=([.55, .17, .17, 1]))  #

        self.grid = GridLayout(cols=2, size_hint=(None, 2))
        self.addbtn = Button(
            text='Add to flame-',
            font_size='50dp',
            color = (0, 0, 0, 1),
            size_hint=(None, None),
            height=int(Window.height)/6,
            width=int(Window.width)/2,
            pos_hint={'center_x': .50}
        )
        self.addbtn.bind(on_press=self.add)

        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit_add)

        self.btn1 = Button(
            text='+ 1',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .1, 'center_y': .3}
        )
        self.btn1.bind(on_press=self.add_button)

        self.btn5 = Button(
            text='+ 5',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .1, 'center_y': .1}
        )
        self.btn5.bind(on_press=self.add_button)

        self.btn10 = Button(
            text='+ 10',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .3}
        )
        self.btn10.bind(on_press=self.add_button)
        self.material_grid = GridLayout(
            cols=1,
            size_hint_x=(None),
            width=int(Window.width)/2.32
            )
        self.build_material_grid()

        self.fuel_grid = GridLayout(
            cols=1,
            size_hint_x=(None),
            width=int(Window.width)/2.32
            )
        # put all in
        self.build_fuel_grid()
        self.relative = RelativeLayout()
        self.grid.add_widget(self.material_grid)
        self.grid.add_widget(self.fuel_grid)
        self.selection_scroll.add_widget(self.grid)
        self.relative.add_widget(self.selection_scroll)
        self.relative.add_widget(self.exitbtn)
        self.relative.add_widget(self.addbtn)
        self.add_stuff.add_widget(self.relative)

    def level_furnace(self, event):
        global furnace_level
        engine.store('cobblestone', -(self.cost))
        furnace_level += 1
        self.levelqtn.text = 'Level: %s' % furnace_level
        self.remove_widget(self.levelqtn)
        self.add_widget(self.levelqtn)
        self.remove_widget(self.levelbtn)
        for i in inventory:
            if i[0] == 'cobblestone' and i[1] >= self.cost:
                self.add_widget(self.levelbtn)

    def exiting_popup(self, event):
        sm.switch_to(MainScreen())

        # Clock.schedule_interval(self.leaving, 0.1)
        # Clock.schedule_interval(self.starting, 0.4)

    def add_button(self, event):
        for x in range(event.quantity):
            if self.selected_quantity < self.possible_quantity:
                self.selected_quantity += 1
        self.addbtn.text = 'Add to flame-%s' % self.selected_quantity

    def exit_add(self, event):
        self.add_stuff.dismiss()

    def add(self, event):
        global time_left_cooking
        log_error = False
        fuel_check = Image(
            size_hint=(None, None),
            height=Window.height/11,
            width=Window.width/11,
            source='materialimg/check.png',
            pos_hint={'center_x': .79, 'center_y': .93}
        )
        material_check = Image(
            size_hint=(None, None),
            height=Window.height/11,
            width=Window.width/11,
            source='materialimg/check.png',
            pos_hint={'center_x': .4, 'center_y': .93}
        )
        try:
            if self.selected_type == 'fuel':
                self.fuel = self.selected_item
                self.fuel_quantity = self.selected_quantity
                self.relative.remove_widget(fuel_check)
                self.relative.add_widget(fuel_check)
            else:
                self.material = self.selected_item
                self.material_quantity = self.selected_quantity
                self.relative.remove_widget(material_check)
                self.relative.add_widget(material_check)
        except AttributeError:
            pass
        
        if self.material == 'log' and self.fuel == 'log':
            total = self.material_quantity + self.fuel_quantity
            for i in inventory:
                if i[0] == 'log' and i[1] < total:
                    log_error = True
                

        if log_error:
            self.addbtn.text = 'Error'

        elif self.fuel and self.material:
            self.is_cooking = True
            self.start_timer()
            self.add_stuff.dismiss()

    def add_material(self, event):
        if is_cooking:
            pass  # we need to change the color to red when it starts if cookin
        else:
            self.add_stuff.open()

    def material_callback(self, event):
        self.relative.remove_widget(self.btn1)
        self.relative.remove_widget(self.btn5)
        self.relative.remove_widget(self.btn10)
        self.selected_item = event.material
        self.selected_type = event.type
        self.possible_quantity = event.quantity
        try:
            # set other selected button back to other color
            self.selected_event.background_color = (1, 1, 1, 1)
        except AttributeError:
            pass
        self.selected_event = event
        # set new event to purple
        event.background_color=(1, 0, 1, 1)
        self.selected_quantity = 1
        if event.quantity >= self.selected_quantity + 1:
            self.relative.add_widget(self.btn1)
        if event.quantity >= self.selected_quantity + 5:
            self.relative.add_widget(self.btn5)
        if event.quantity >= self.selected_quantity + 10:
            self.relative.add_widget(self.btn10)
        self.btn1.quantity=1
        self.btn5.quantity=5
        self.btn10.quantity=10
        self.addbtn.text = 'Add to flame-%s' % self.selected_quantity
        self.possible_quantity = event.quantity

        # Green check next to material

    def fuel_callback(self, event):
        self.relative.remove_widget(self.btn1)
        self.relative.remove_widget(self.btn5)
        self.relative.remove_widget(self.btn10)
        self.selected_item = event.fuel
        self.selected_type = event.type
        self.possible_quantity = event.quantity
        try:
            # set other selected button back to other color
            self.selected_event.background_color = (1, 1, 1, 1)
        except AttributeError:
            pass
        self.selected_event = event
        # set new event to purple
        event.background_color=(1, 0, 1, 1)
        self.selected_quantity = 1
        if event.quantity >= self.selected_quantity + 1:
            self.relative.add_widget(self.btn1)
        if event.quantity >= self.selected_quantity + 5:
            self.relative.add_widget(self.btn5)
        if event.quantity >= self.selected_quantity + 10:
            self.relative.add_widget(self.btn10)
        self.btn1.quantity=1
        self.btn5.quantity=5
        self.btn10.quantity=10
        self.addbtn.text = 'Add to flame-%s' % self.selected_quantity
        self.possible_quantity = event.quantity

        # Green check next to fuel

    def build_material_grid(self):
        # 1 col of buttons -- materials
        self.label = Label(
            text='Material',
            font_size='40dp',
            size_hint=(None, None),
            height=Window.height/8.0,
            width=Window.width/2.32
        )
        self.material_grid.add_widget(self.label)
        for x in inventory:
            for i in cook_output:
                if x[0] == i[0] and x[1] > 0:
                    bstext = i[0]
                    bstext = bstext.replace("_", " ")
                    self.btn = Button(
                        text=bstext,
                        font_size='40dp',
                        size_hint=(.4, .4)
                    )
                    self.btn.item=i[0]
                    self.btn.material = i[0]
                    self.btn.quantity = x[1]
                    self.btn.type = 'material'
                    self.btn.bind(on_press=self.material_callback)
                    self.material_grid.add_widget(self.btn)
        self.material_grid.add_widget(Button(background_color=(0, 0, 0, 1), size_hint=(.4, .4)))

    def build_fuel_grid(self):
        # 1 col of buttons -- fuel
        self.label = Label(
            text='Fuel',
            font_size='40dp',
            size_hint=(None, None),
            height=Window.height/8.0,
            width=Window.width/2.32
        )
        self.fuel_grid.add_widget(self.label)
        for i in inventory:
            for x in fuel_quantity:
                if x[0] == i[0] and i[1] >= 1:
                    bstext = i[0]
                    bstext = bstext.replace("_", " ")
                    self.btn = Button(
                        text=bstext,
                        font_size='40dp',
                        size_hint=(.4, .4)
                    )
                    self.btn.item=i[0]
                    self.btn.fuel = i[0]
                    self.btn.quantity = i[1]
                    self.btn.type = 'fuel'
                    self.btn.bind(on_press=self.fuel_callback)
                    self.fuel_grid.add_widget(self.btn)
        

        for i in equipment:
            for x in fuel_quantity:
                if x[0] == i[0]:
                    bstext = i[0]
                    bstext = bstext.replace("_", " ")
                    self.btn = Button(
                        text=bstext,
                        font_size='40dp',
                        size_hint=(.4, .4)
                        #height=Window.height/4.0,
                        #width=Window.width/2.32
                    )
                    self.item=i[0]
                    self.btn.fuel = i[0]
                    self.btn.quantity = 1
                    self.btn.type = 'fuel'
                    self.btn.bind(on_press=self.fuel_callback)
                    self.fuel_grid.add_widget(self.btn)
        self.fuel_grid.add_widget(Button(background_color=(0, 0, 0, 1), size_hint=(.4, .4)))

    def leaving(self, event):
        Clock.unschedule(self.count_down_text)

    def starting(self, event):
        # CHECK IF HAVE FURNACE, IF NOT,
        # switch to no_furnace screen
        global main_text
        can_cook = False
        have_fuel = False
        furnace_have = False
        for i in inventory:
            if i[0] == 'furnace':
                furnace_have = True
        for x in inventory:
            for i in cook_output:
                if x[0] == i[0] and x[1] > 0:
                    can_cook = True

        for i in inventory:
            for x in fuel_quantity:
                if x[0] == i[0] and i[1] >= 1:
                    have_fuel = True

        for i in equipment:
            for x in fuel_quantity:
                if x[0] == i[0] and i[1] >= 1:
                    have_fuel = True
        if furnace_have:
            if can_cook and have_fuel:
                pass
                global is_cooking
                if is_cooking:
                    Clock.schedule_interval(self.count_down_text, 1)
            else:
                main_text = "You don't have\nanything to cook"
                sm.switch_to(MainScreen())
        else:
            main_text = 'Build a Furnace first'
            sm.switch_to(MainScreen())

    """ Where it starts cooking with x materials and fuel
     uses engine.countdown to keep track of the time
     when going between separate screens
     also where an animation will be, described in the
     minetextdoc.odt file,  The animation will be of """
    def start_timer(self):
        global cooking_chart
        cooking_chart = [
            self.material,
            self.material_quantity,
            self.fuel,
            self.fuel_quantity,
        ]
        a = cooking_chart
        material = a[0]
        material_quantity = a[1]
        fuel = a[2]
        fq = a[3]
        for i in fuel_quantity:
            if i[0] == fuel:
                raw_fuel = i[1] * fq
                cooking_chart.append(i[1])
                fuel_value = i[1]
        if raw_fuel > material_quantity:
            # change fuel quantity
            fq = fq - ((raw_fuel - material_quantity) / fuel_value)
            cooking_chart = [material, material_quantity, fuel, fq]
        else:
            # change material quantity
            material_quantity = raw_fuel
            cooking_chart = [material, material_quantity, fuel, fq]
        engine.store(material, -(material_quantity))
        engine.store(fuel, -(fq))
        Clock.schedule_interval(engine.count_down, 1)

    def count_down_text(self, dt):
        global is_cooking
        global time_left_cooking
        if is_cooking:
            self.time_label.text = str("Time Left: " +str(time_left_cooking))
            self.cookbtn.text = 'Cooking'
            self.cookbtn.background_color = (1.66, 0.47, 0.47, 62)
            Clock.schedule_once(self.rolling_label, .25)
            Clock.schedule_once(self.rolling_label, .50)
            Clock.schedule_once(self.rolling_label, .70)
            Clock.schedule_once(self.rolling_label_reset, 1)
        else:
            self.time_label.text = ''
            self.cookbtn.text = 'Cook'
            self.cookbtn.background_color = (1.81, 1.86, 2.26, 1)

    def rolling_label(self, dt):
        _text = str(self.cookbtn.text + '.')
        self.cookbtn.text = _text

    def rolling_label_reset(self, dt):
        self.cookbtn.text = 'Cooking'
        self.cookbtn.background_color = (1.66, 0.47, 0.47, 1)

    def exit_screen(self, event):
        global main_text
        global _just_exited_furnace
        _just_exited_furnace = False
        main_text = 'Back from Cooking...'
        sm.switch_to(MainScreen())


class Sleep(Screen):  # animate
    def __init__(self, **kwargs):
        super(Sleep, self).__init__(**kwargs)
        global night
        self.night = night
        self.have_bed = False
        for i in inventory:
            if i[0] == 'bed':
                self.have_bed = True
        self.btn1 = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.btn2 = Button(
            text='Sleep',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/7.0,
            width=int(Window.width)/2,
            pos_hint={'center_x': .5, 'center_y': .3}
        )
        self.label = Label(
            text='',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/7.0,
            width=int(Window.width),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.add_widget(self.label)
        self.btn1.bind(on_press=self.callback)
        self.add_widget(self.btn1)
        self.btn2.bind(on_press=self.start)
        self.add_widget(self.btn2)

    def callback(self, event):
        global main_text
        main_text = 'Back from sleeping...'
        sm.switch_to(MainScreen())

    def start(self, event):
        global main_text
        global farming_started
        if self.have_bed == False:
            self.label.text="You can't sleep on the ground, silly"
            self.btn2.disabled = True
        elif self.night == False:
            self.label.text="No naps allowed, sleep at night..."
            self.btn2.disabled = True
        else:
            stat.misc('sleep', 1)
            self.label.text=(str(engine.tick(100)))
            if farming_started:
                global current_time
                current_time -= 300
                Clock.schedule_once(FarmEngine.interval, .5)
            self.btn2.disabled = True


"""FARM @@@@ FARM @@@@ FARM @@@@
FARM @@@@ FARM @@@@ FARM @@@@
FARM @@@@ FARM @@@@ FARM @@@@
FARM @@@@ FARM @@@@ FARM @@@@"""

# Reference to farm
    # ........
        # ['wheat', 1, 500, 0, 0, 0, 0, 3600, 1, dirt, 50000, 150]
        # 0 name
        # 1 type,
        # 2 is built,
        # 3 cost,
        # 4 has_water,  ...
        # 5 ready to be harvested,
        # 6 time_passed,
        # 7 time_waterd
        # 8 time needs water ,
        # 9 level ,
        # 10 material
        # 11 chance of storm breaking
        # 12 distance from river


class Farm(object):
    def __init__(self, farm):
        farm = object
        # initialized after variables are changed
        # or to check variables
        self.type = farm[0]
        self.is_built = farm[1]
        self.cost = farm[2]
        self.has_water = farm[3]
        self.harvestable = farm[4]
            # ready_to_be_harvested

        self.time_passed = farm[5]
        self.time_watered = farm[6]
        self.time_needs_water = farm[7]
            # time till harvestable

        self.level = farm[8]
        self.material = farm[9]
        self.storm = farm[10]
            # chance_of_storm_breaking

        self.name = farm[11]
        self.distance = farm[12]
            # distance from river

    def wheat_farm(self):
        pass

    def log_farm(self):
        pass

    def skeleton_farm(self):
        pass


class FarmEngine(object):
    """Good ole farmie, saved the day again!"""
    def __init__(self):
        global selected_farm

    # runs every 10 seconds
    def interval(self):
        global current_time
        global time_passed_storm
        global all_farms
        global farming_started
        need_water = False
        need_harvest = False
        storm_destoryed = False
        time_now = math.floor(time.time())
        time_passed = (time_now - current_time) / 10
        # for every 10 seconds passed
        for x in range(int(time_passed)):
            time_passed_storm += 10

            for i in all_farms:
                if i[12] == 0:
                    i[3] = 1
                    i[5] = -1000
                    i[6] += 10
                elif i[3] == 1:  # add water
                    i[6] += 10  # time_watered
                    i[5] += 10

                if i[6] >= i[7]:
                    i[4] = 1  # harvestable
                    need_harvest = True
                    i[6] = 0  # time_watered
                    i[7] = random.randint(
                        (500 * (i[8]/2)), (1250 * (i[8]/2)))
                        # time_needs_water

                if i[4] == 0 and i[3] == 1 and i[5] >= 1 and i[12] > 0:
                    i[5] = 0
                    i[3] = 0
                    need_water = True

                # %20 chance of a storm passing
                # each farm every hour
                if time_passed_storm >= 1800 and (
                   random.randint(0, 100) < 20):
                    if random.randint(0, 1000000) < i[10]:
                        storm_destoryed = True
                        all_farms.remove(i)
                    if len(all_farms) == 0:
                        Clock.unschedule(FarmEngine.interval)
                        farming_started = False

            if time_passed_storm >= 1800:
                time_passed_storm = 0

        msg = ''
        if storm_destoryed:
            msg += 'A farm was destoyed in a storm!\n\n'
        if need_harvest:
            msg += 'A farm needs to be harvested!\n\n'
        if need_water:
            msg += 'A farm is ready to be watered!\n\n'

        if storm_destoryed or need_harvest or need_water:
            global farmx_label
            farmx_label = FarmPopup()
            farmx_label.text = msg
            Window.add_widget(farmx_label)

        current_time = time_now


class FarmMenu(Screen):
    def __init__(self, **kwargs):
        super(FarmMenu, self).__init__(**kwargs)
        global selected_farm
        #self.bind(on_enter=self.starting)
        self.buildbtn = Button(
            text='Build',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .13, 'center_y': .89}
        )
        self.buildbtn.bind(on_press=self.build_farm)

        self.destroybtn = Button(
            text='Destroy',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .13, 'center_y': .69}
        )
        self.destroybtn.bind(on_press=self.destroy_farm)

        self.irrigatebtn = Button(
            text='Irrigate',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .88, 'center_y': .29}
        )
        self.irrigatebtn.bind(on_press=self.irrigate_farm)

        self.levelbtn = Button(
            text='Level up',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .88, 'center_y': .89}
        )
        self.levelbtn.bind(on_press=self.level_farm)

        self.harvestbtn = Button(
            text='Harvest',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .88, 'center_y': .49}
        )
        self.harvestbtn.bind(on_press=self.harvest_farm)

        self.waterbtn = Button(
            text='Water',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .88, 'center_y': .69}
        )
        self.waterbtn.bind(on_press=self.water_farm)

        self.main_label = Label(
            text="",
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .5, 'center_y': .40}
        )
        self.add_widget(self.main_label)

        self.selectbtn = Button(
            text='Select a farm',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/2.8,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .5, 'center_y': .1}
        )
        self.selectbtn.bind(on_press=self.select_farm)
        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit)

        self.exitbtn2 = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn2.bind(on_press=self.leaving)
        self.add_widget(self.exitbtn2)

        self.buildbtn2 = Button(
            text='Build a farm!',
            font_size='90dp',
            size_hint=(None, None),
            width=int(Window.width)/1.5,
            height=int(Window.height)/4,
            background_color=(0.84, 1.42, 0.34, 1),
            pos_hint={'center_x': .5, 'center_y': .5}
        )

    # call this to refresh the page
    # on exit of the selected_farm
    #def starting(self, event):
        global selected_farm
        global farming_started
        self.clear_event()
        # remove
        # main label
        # remove
        if farming_started:
            self.add_widget(self.selectbtn)
            self.add_widget(self.buildbtn)
            self.add_widget(self.destroybtn)
            self.destroybtn.disabled = True
            self.add_widget(self.levelbtn)
            self.levelbtn.disabled = True
            self.add_widget(self.harvestbtn)
            self.harvestbtn.disabled = True
            self.add_widget(self.waterbtn)
            self.waterbtn.disabled = True
            self.add_widget(self.irrigatebtn)
            self.irrigatebtn.disabled = True
            if selected_farm:
                self.selected_label = SelectLabel(
                    font_size='35dp',
                    size_hint=(None, None),
                    width=int(Window.width)/4,
                    height=int(Window.height)/6,
                    size_hint_x=None,
                    pos_hint={'center_x': .505, 'center_y': .79}
                )
                self.selected_label.farm = selected_farm
                self.remove_widget(self.selected_label)
                self.add_widget(self.selected_label)
                self.destroybtn.disabled = False
                self.levelbtn.disabled = False
                if selected_farm[4] == 1:
                    self.harvestbtn.disabled = False
                elif selected_farm[12] > 0:
                    self.waterbtn.disabled = False
                if selected_farm[8] >= 3 and selected_farm[12] > 0:
                    self.irrigatebtn.disabled = False
        else:
            self.buildbtn2.bind(on_press=self.build_farm)
            self.add_widget(self.buildbtn2)

    # clears selected farm when leaving
    def leaving(self, event):
        global selected_farm
        self.clear_event()
        selected_farm = None
        sm.switch_to(MainScreen())

    def select_farm(self, event):
        self.clear_event()
        sm.switch_to(SelectFarm())

    def water_farm(self, event):
        self.clear_event()
        sm.switch_to(WaterFarm())

    def harvest_farm(self, event):
        self.clear_event()
        global selected_farm
        farm = selected_farm
        amount_received = int(farm[8] * 10 * (float(farm[8])/3))
        engine.store(farm[0], amount_received)
        stat.harvest(farm[0], amount_received)
        for i in all_farms:
            if i[11] == farm[11]:
                i[4] = 0
        self.main_label.text = str(
                'You harvested\n%s %s' %
                (amount_received, farm[0]))
        self.harvestbtn.disabled = True

    def build_farm(self, event):
        self.clear_event()
        sm.switch_to(BuildFarm())

    def level_farm(self, event):
        self.clear_event()
        sm.switch_to(LevelFarm())

    def irrigate_farm(self, event):
        self.clear_event()
        sm.switch_to(IrrigateFarm())

    def destroy_farm(self, event):
        self.clear_event()
        sm.switch_to(DestroyFarm())

    def exit(self, event):
        self.clear_event()
        sm.switch_to(MainScreen())

    def clear_event(self):
        try:
            global event578
            event578.cancel()
        except NameError:
            pass

    # calls the instance of a farm based on its list
    # ........
        # ['wheat', 1, 500, 0, 0, 0, 0,
        #  3600, 1, dirt, 50000, '\str', 150]
        # 0 type,
        # 1 is built,
        # 2 cost,
        # 3 has_water,  ...
        # 4 ready to be harvested,
        # 5 time_passed_while_watered,
        # 6 time_waterd
        # 7 time needs water ,
        # 8 level ,
        # 9 material
        # 10 chance of storm breaking
        # 11 name
        # 12 distance from river


class DestroyFarm(Screen):
    def __init__(self, **kwargs):
        super(DestroyFarm, self).__init__(**kwargs)
        self.alert_label = Label(
            text='Are you sure you\nwant to destroy your farm?',
            font_size='50dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .5, 'center_y': .75}
        )
        self.add_widget(self.alert_label)
        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit_destroy)
        self.add_widget(self.exitbtn)

        self.destroybtn = Button(
            text='Destroy',
            font_size='80dp',
            size_hint=(None, None),
            width=int(Window.width)/2,
            height=int(Window.height)/5,
            size_hint_x=None,
            background_color=(0.04, 1.65, 0.63, 1),
            pos_hint={'center_x': .5, 'center_y': .2}
        )
        self.destroybtn.bind(on_press=self.destroy_farm)
        self.add_widget(self.destroybtn)

    def destroy_farm(self, event):
        global selected_farm
        global farming_started
        for i in all_farms:
            if selected_farm[11] == i[11]:
                all_farms.remove(i)
                sm.switch_to(FarmMenu())
        if len(all_farms) == 0:
            Clock.unschedule(FarmEngine.interval)
            farming_started = False
        selected_farm = None

    def exit_destroy(self, event):
        sm.switch_to(FarmMenu())


class LevelFarm(Screen):
    def __init__(self, **kwargs):
        super(LevelFarm, self).__init__(**kwargs)
        self.bind(on_enter=self.start)

    def start(self, dt):
        self.bucket_count = 0
        for i in all_farms:
            if i[11] == selected_farm[11]:
                self.farm = i

        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit_level)
        self.add_widget(self.exitbtn)

        self.levelbtn = Button(
            text='Level Up',
            font_size='80dp',
            size_hint=(None, None),
            width=int(Window.width)/2,
            height=int(Window.height)/5,
            size_hint_x=None,
            background_color=(0.04, 1.65, 0.63, 1),
            pos_hint={'center_x': .5, 'center_y': .2}
        )
        self.levelbtn.bind(on_press=self.level)
        self.add_widget(self.levelbtn)

        self.alert_label = Label(
            text='Be sure to harvest\nbefore leveling up!',
            font_size='50dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .5, 'center_y': .75}
        )
        self.add_widget(self.alert_label)

    def exit_level(self, event):
        sm.switch_to(FarmMenu())

    def level(self, event):
        global selected_farm
        global money
        x = selected_farm
        base_level_cost = [10, 10, 4, 10]
        level_cost = [i * 2 * x[8] for i in base_level_cost]
        have_material = False
        have_stone = False
        have_dirt = False
        have_money = False
        materialq = 0
        stoneq = 0
        dirtq = 0
        material = x[9]
        for i in inventory:
            if i[0] == (x[9]) and i[1] >= level_cost[0]:
                have_material = True
            if i[0] == (x[9]):
                materialq = i[1]
            if i[0] == 'stone' and i[1] >= level_cost[1]:
                have_stone = True
            if i[0] == 'stone':
                stoneq = i[1]
            if i[0] == ('dirt') and i[1] >= level_cost[2]:
                have_dirt = True
            if i[0] == 'dirt':
                dirtq = i[1]
        if money > level_cost[3]:
            have_money = True

        if have_material and have_stone and have_dirt and have_money:
            for i in all_farms:
                if x[11] == i[11]:
                    level_farm = True
                    i[8] += 1
                    i[4] = 0

                    engine.store((x[9]), -(level_cost[0]))
                    engine.store('stone', -(level_cost[1]))
                    engine.store('dirt', -(level_cost[2]))
                    engine.money_add(-(level_cost[3]))
                    self.alert_label.text = 'Farm leveled!'

        else:
            msg = ''
            if not have_material:
                msg += 'Not enough %s (%s/%s)\n' % (
                        material, materialq, level_cost[0])
            if not have_stone:
                msg += 'Not enough stone (%s/%s)\n' % (
                    stoneq, level_cost[1])
            if not have_dirt:
                msg += 'Not enough dirt (%s/%s)\n' % (
                    dirtq, level_cost[2])
            if not have_money:
                msg += 'Not enough money (%s/%s)' % (
                    money, level_cost[3])

            self.alert_label.text = msg


class SelectFarm(Screen):
    def __init__(self, **kwargs):
        super(SelectFarm, self).__init__(**kwargs)
        self.bind(on_enter=self.build_scroll)

    def build_scroll(self, event):
        global selected_farm
        self.scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height),
            pos_hint={'center_x': .5},
            bar_color=([.81, .55, .55, 1]),  #
            bar_inactive_color=([.55, .17, .17, 1])  #
        )

        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit_select)

        self.mat_grid = GridLayout(
            size_hint=(None, 2),
            cols=1
        )
        self.mat_grid.add_widget(Label(
            text='My Farms',
            font_size='50dp',
            size_hint_y=(None),
            height=(Window.height/8.0)))
        for i in all_farms:  # i0
            btn = SelectButton()
            btn.farm = i
            if selected_farm and i[11] == selected_farm[11]:
                btn.background_color=(1.43, 1.98, 0.53, 1)
            btn.bind(on_press=self.select_callback)
            self.mat_grid.add_widget(btn)
        for i in range(2):
            label = Label()
            self.mat_grid.add_widget(label)
        self.scroll.add_widget(self.mat_grid)
        self.add_widget(self.scroll)
        self.add_widget(self.exitbtn)

    def select_callback(self, event):
        global selected_farm
        selected_farm = event.farm
        global event578
        event578.cancel()
        sm.switch_to(FarmMenu())

    def exit_select(self, event):
        global event578
        event578.cancel()
        sm.switch_to(FarmMenu())


class WaterFarm(Screen):
    def __init__(self, **kwargs):
        super(WaterFarm, self).__init__(**kwargs)
        global selected_farm
        self.bind(on_enter=self.start)

    def start(self, dt):
        self.bucket_count = 0
        for i in all_farms:
            if i[11] == selected_farm[11]:
                self.farm = i

        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit_water)
        self.add_widget(self.exitbtn)

        self.waterbtn = Button(
            text='Water',
            font_size='80dp',
            size_hint=(None, None),
            width=int(Window.width)/2,
            height=int(Window.height)/5,
            size_hint_x=None,
            background_color=(0.64, 1.64, 2.23, 1),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.waterbtn.bind(on_press=self.water)
        self.add_widget(self.waterbtn)

        self.bucketlabel = Label(
            font_size='50dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .5, 'center_y': .68}
        )
        for i in inventory:
            if i[0] == 'water_bucket':
                self.bucket_count = i[1]
        self.bucketlabel.text = ('Water Buckets(%s)'
                                 % self.bucket_count)
        self.add_widget(self.bucketlabel)

    def water(self, event):
        watered = False
        for i in inventory:
            if i[0] == 'water_bucket' and i[1] > 0:
                engine.store("water_bucket", -1)
                engine.store("bucket", 1)
                self.bucket_count -= 1
                for i in all_farms:
                    if self.farm[11] == i[11]:
                        i[5] -= 50
                        i[3] = 1
                # water selected farm here
                watered = True
        self.bucketlabel.text = ('Water Buckets(%s)'
                                 % self.bucket_count)

    def exit_water(self, event):
        sm.switch_to(FarmMenu())


class IrrigateFarm(Screen):
    def __init__(self, **kwargs):
        super(IrrigateFarm, self).__init__(**kwargs)
        self.bind(on_enter=self.start)

    def start(self, dt):
        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit_irrigate)
        self.add_widget(self.exitbtn)

        self.waterbtn = Button(
            text='Irrigate',
            font_size='80dp',
            size_hint=(None, None),
            width=int(Window.width)/2,
            height=int(Window.height)/5,
            size_hint_x=None,
            background_color=(0.64, 1.64, 2.23, 1),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.waterbtn.bind(on_press=self.irrigate)
        self.add_widget(self.waterbtn)

        self.notify1 = Label(
            font_size='50dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .5, 'center_y': .78}
        )
        self.notify2 = Label(
            font_size='50dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            pos_hint={'center_x': .5, 'center_y': .68}
        )
        self.add_widget(self.notify1)
        self.add_widget(self.notify2)

    def irrigate(self, event):
        global selected_farm
        distance = selected_farm[12]
        qlogs = int(distance/1.5)
        qiron = int(distance/1.8)
        have_logs = 0
        have_iron = 0
        has_iron = False
        has_logs = False
        for i in inventory:
            if i[0] == 'log':
                have_logs = i[1]
            elif i[0] == 'iron':
                have_iron = i[1]
        
        if have_logs >= qlogs:
            has_logs = True
        if have_iron >= qiron:
            has_iron = True

        if has_iron and has_logs:
            selected_farm[12] = 0
            selected_farm[5] = -1000
            selected_farm[3] = 1
            engine.store('log', int(-qlogs))
            engine.store('iron', int(-qiron))
            self.remove_widget(self.waterbtn)
            self.notify1.text = ("Farm irrigated!")
        else:
            if not has_logs:
                self.notify1.text = ('Not enough logs(%s/%s)') %(
                                     have_logs, qlogs)
            if not has_iron:
                self.notify2.text = ('Not enough iron(%s/%s)') %(
                                     have_iron, qiron)

    def exit_irrigate(self, event):
        sm.switch_to(FarmMenu())


class BuildFarm(Screen):
    def __init__(self, **kwargs):
        super(BuildFarm, self).__init__(**kwargs)
        self.bind(on_enter=self.test)
        # add items to grid here

    def test(self, event):
        Clock.schedule_once(self.build_material_scroll)

    def build_material_scroll(self, event):
        self.scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height),
            pos_hint={'center_x': .5},
            bar_color=([.81, .55, .55, 1]),  #
            bar_inactive_color=([.55, .17, .17, 1])  #
        )

        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.exit_build)

        self.mat_grid = GridLayout(
            size_hint=(None, 2),
            cols=1
        )
        for i in farm_materials:  # i0
            bstext = str('%s' % i[0])
            bstext = bstext.replace("_", " ")
            btn = Button(
                text=bstext,
                font_size='40dp',
                size_hint_x=None,
                width=Window.width/1.11
            )
            btn.item = i[0]
            btn.bind(on_press=self.material_btn_callback)
            self.mat_grid.add_widget(btn)
        for i in range(2):
            label = Label()
            self.mat_grid.add_widget(label)
        self.scroll.add_widget(self.mat_grid)
        self.add_widget(self.scroll)
        self.add_widget(self.exitbtn)

    def material_btn_callback(self, event):
        enough_dirt = False
        enough_stone = False
        enough_material = False
        for i in inventory:
            if i[0] == event.item:
                if i[1] < 100:
                    pass
                else:
                    enough_material = True
            if i[0] == 'stone' and i[1] >= 80:
                if event.item == 'stone':
                    if i[1] >= 180:
                        enough_stone = True
                else:
                    enough_stone = True
            if i[0] == 'dirt' and i[1] >= 40:
                enough_dirt = True

        if not enough_material:
            event.text = "You don't have enough(100)"
        else:

            if enough_dirt and enough_material and enough_stone:
                self.remove_widget(self.scroll)
                self.build_farm(event)
            else:
                self.remove_widget(self.scroll)
                self.label = Label(
                    font_size='60dp',
                    size_hint=(None, None),
                    height=Window.height,
                    width=Window.width
                )
                self.label.text = ''
                if not enough_dirt:
                    self.label.text += "\n  You don't have 40 dirt"
                if not enough_stone:
                    self.label.text += "\n  You don't have 80 stone"
                self.add_widget(self.label)

    def build_farm(self, event):
        self.grid = GridLayout(
            cols=1,
            size_hint=(None, None),
            height=Window.height/1.2,
            width=Window.width/1.2,
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.btn1 = Button(
            text='Crop farm',
            font_size='45dp',
        )
        self.btn1.item = event.item
        self.btn1.bind(on_press=self.build_crop_farm)
        self.btn2 = Button(
            text='Animal farm/na',
            font_size='45dp',
        )
        self.btn2.item = event.item
        self.btn2.bind(on_press=self.build_animal_farm)
        self.btn3 = Button(
            text='Monster farm/na',
            font_size='45dp',
        )
        self.btn3.item = event.item
        self.btn3.bind(on_press=self.build_monster_farm)
        self.grid.add_widget(self.btn1)
        self.grid.add_widget(self.btn2)
        self.grid.add_widget(self.btn3)
        self.add_widget(self.grid)
        self.remove_widget(self.exitbtn)
        self.add_widget(self.exitbtn)

    def build_crop_farm(self, event):
        global money
        self.remove_widget(self.grid)
        self.remove_widget(self.exitbtn)
        self.money_label = Label(
            text='You have $%s' % money,
            font_size='50dp',
            pos_hint={'center_x': .5, 'center_y': .95},
        )
        grid = GridLayout(cols=1, size_hint=(None, 2))
        self.scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            pos_hint={'center_x': .5, 'center_y': .4},
            bar_color=([.81, .55, .55, 1]),  #
            bar_inactive_color=([.55, .17, .17, 1])  #
        )
        for i in CropFarmType:
            bstext = "%s | $%s" % (i[0], i[1])
            btn = Button(
                text=bstext,
                font_size='50dp',
                size_hint_x=(None),
                width=Window.width/1.11
            )
            btn.item = event.item
            btn.type = i[0]
            btn.price = i[1]
            btn.bind(on_press=self.build_crop_farm2)
            grid.add_widget(btn)
        self.scroll.add_widget(grid)
        self.add_widget(self.scroll)
        self.add_widget(self.exitbtn)
        self.add_widget(self.money_label)

    def build_crop_farm2(self, event):
        global money
        if money >= event.price:
            self.remove_widget(self.scroll)
            self.remove_widget(self.money_label)
            self.nameinput = MyTextInput(
                font_size='50dp',
                multiline=False,
                size_hint=(None, None),
                width=Window.width/1.1,
                height=200,
                pos_hint={'center_x': .5, 'center_y': .7}
            )
            self.build_label = Label(
                text='What would you like\nto call your farm?',
                pos_hint={'center_x': .5, 'center_y': .87},
                font_size='40dp'
            )
            self.build_btn = Button(
                text='BUILD',
                font_size='70dp',
                pos_hint={'center_x': .5, 'center_y': .4},
                size_hint=(None, None),
                background_color=(0.84, 1.42, 0.34, 1),
                width=Window.width/1.5,
                height=Window.height/7.5

            )
            self.build_btn.item = event.item
            self.build_btn.type = event.type
            self.build_btn.price = event.price
            self.build_btn.base = 'crop'
            self.build_btn.bind(on_press=self.build_process)
            self.add_widget(self.build_btn)
            self.add_widget(self.build_label)
            self.add_widget(self.nameinput)

        else:
            event.text = 'Not enough money(%s)' % event.price

    def build_animal_farm(self, event):
        print(event.item)
        print("Not added")

    def build_monster_farm(self, event):
        print(event.item)
        print("Not added")

    def build_process(self, event):
        unique = True
        for i in all_farms:
            if str(self.nameinput.text) == i[11]:
                unique = False

        if not unique:
            self.build_label.text = (
                'You already have a farm with that name')
        else:
            global farming_started
            self.remove_widget(self.build_btn)
            self.remove_widget(self.build_label)
            self.remove_widget(self.nameinput)
            farm = []
            farm.append(event.type)  # type  0
            farm.append(1)  # is_build 1
            farm.append(event.price)  # cost 2
            farm.append(0)  # has_water 3
            farm.append(0)  # harvestable 4
            farm.append(0)  # time_passed
            farm.append(0)  # time_passed_while_watered
            farm.append(random.randint(1000, 2000))  # time_needs_water
            farm.append(1)  # level
            farm.append(event.item)  # material
            for i in farm_materials:
                if i[0] == event.item:
                    chance_of_storm = i[1]
            farm.append(chance_of_storm)  # chance of storm breaking
            farm.append(str(self.nameinput.text))  # name
            # distance from river
            distance = random.randint(20, 300)
            farm.append(distance)
            engine.money_add(-(event.price))
            engine.store(farm[8], -100)
            engine.store('stone', -80)
            engine.store('dirt', -40)
            all_farms.append(farm)
            if farming_started:
                pass
            else:
                farmie = FarmEngine()
                Clock.schedule_interval(FarmEngine.interval, 10)
                farming_started = True
                global farmx_label
                farmx_label = FarmPopup()
                farmx_label.text = 'A farm needs water'
                Window.add_widget(farmx_label)
            global selected_farm
            selected_farm = farm
            sm.switch_to(FarmMenu())

    def exit_build(self, event):
        sm.switch_to(FarmMenu())  # farm menu!

    # calls the instance of a farm based on its list
    # ........
        # ['wheat', 1, 500, 0, 0, 0, 0,
        # 3600, 1, dirt, 50000, '\str', 150]
        # 0 type,
        # 1 is built,
        # 2 cost,
        # 3 has_water,  ...
        # 4 ready to be harvested,
        # 5 time_passed_while_watered,
        # 6 time_waterd
        # 7 time needs water ,
        # 8 level ,
        # 9 material
        # 10 chance of storm breaking
        # 11 name
        # 12 distance from river


class MyTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # limit to 17 chars
        substring = substring[:17 - len(self.text)]
        return super(MyTextInput, self).insert_text(
            substring, from_undo=from_undo)


class FarmPopup(Label):
    def __init__(self, **kwargs):
        super(FarmPopup, self).__init__(**kwargs)
        self.font_size = '45dp'
        self.pos = [0, -300]
        self.color = ([.27, .72, .39, 1])
        Clock.schedule_interval(self.move, .01)

    def move(self, dt):
        global xvbbb
        xvbbb += 2.5
        self.pos = [0, xvbbb]
        if xvbbb >= 350:
            Window.remove_widget(farmx_label)
            Clock.unschedule(self.move)
            xvbbb = -300


class SelectButton(Button):
    def __init__(self, **kwargs):
        super(SelectButton, self).__init__(**kwargs)
        global event578
        self.font_size = '28dp'
        self.size_hint_x = None
        self.size_hint_y = None
        self.height = Window.height/3
        self.width = Window.width/1.11
        Clock.schedule_once(self.define_times, .01)
        Clock.schedule_once(self.interval, .02)
        event578 = Clock.schedule_interval(self.interval, 1)
        # is this unscheduled with multiple farms.

    def define_times(self, dt):
        i = self.farm
        if i[3] == 1:
            # time until harvest
            if i[4] == 0:
                self.xz = i[7] - i[6]
            else:
                self.xz = 0
            # time until dry
            self.yz = -i[5]
        elif i[4] == 1:
            self.xz = 0
            self.yz = 0
        else:
            self.xz = 'N/A'

    def interval(self, dt):
        i = self.farm

        if i[3] == 1 and self.yz != 0:
            bstext = ''
            bstext += str(i[11])
            bstext += '\n'
            bstext += str('lvl %s %s farm' % (i[8], i[0]))
            bstext += '\n'
            bstext += str('%s until harvest' % self.xz)
            bstext += '\n'
            bstext += str('%s until dry' % self.yz)
            if i[12] > 0:
                bstext += '\n'
                bstext += str('%s meters from a river' % i[12])
            self.text = bstext
            if self.xz != 0:
                self.xz -= 1
            if self.yz != 0:
                if i[12] > 0:
                    self.yz -= 1
        elif i[4] == 1 or self.xz == 0:
            bstext = ''
            bstext += str(i[11])
            bstext += '\n'
            bstext += str('lvl %s %s farm' % (i[8], i[0]))
            bstext += '\n'
            bstext += str('Ready to harvest!')
            self.text = bstext

        else:
            bstext = ''
            bstext += str(i[11])
            bstext += '\n'
            bstext += str('lvl %s %s farm' % (i[8], i[0]))
            bstext += '\n'
            bstext += str('Needs water!')
            self.text = bstext


class SelectLabel(Label):
    def __init__(self, **kwargs):
        super(SelectLabel, self).__init__(**kwargs)
        global event578
        Clock.schedule_once(self.define_times, .01)
        Clock.schedule_once(self.interval, .02)
        event578 = Clock.schedule_interval(self.interval, 1)
        # is this unscheduled with multiple farms.

    def define_times(self, dt):
        i = self.farm
        if i[3] == 1:
            # time until harvest
            if i[4] == 0:
                self.xz = i[7] - i[6]
            else:
                self.xz = 0
            # time until dry
            self.yz = -i[5]
        elif i[4] == 1:
            self.xz = 0
            self.yz = 0
        else:
            self.xz = 'N/A'

    def interval(self, dt):
        i = self.farm

        if i[3] == 1 and self.yz != 0:
            bstext = ''
            bstext += str(i[11])
            bstext += '\n'
            bstext += str('lvl %s %s farm' % (i[8], i[0]))
            bstext += '\n'
            bstext += str('%s until harvest' % self.xz)
            bstext += '\n'
            bstext += str('%s until dry' % self.yz)
            if i[12] > 0:
                bstext += '\n'
                bstext += str('%s meters from a river' % i[12])
            self.text = bstext
            if self.xz != 0:
                self.xz -= 1
            if self.yz != 0:
                if i[12] > 0:
                    self.yz -= 1
        elif i[4] == 1 or self.xz == 0:
            bstext = ''
            bstext += str(i[11])
            bstext += '\n'
            bstext += str('lvl %s %s farm' % (i[8], i[0]))
            bstext += '\n'
            bstext += str('Ready to harvest!')
            self.text = bstext

        else:
            bstext = ''
            bstext += str(i[11])
            bstext += '\n'
            bstext += str('lvl %s %s farm' % (i[8], i[0]))
            bstext += '\n'
            bstext += str('Needs water!')
            self.text = bstext



"""FARM @@@@ FARM @@@@ FARM @@@@
FARM @@@@ FARM @@@@ FARM @@@@
FARM @@@@ FARM @@@@ FARM @@@@
FARM @@@@ FARM @@@@ FARM @@@@"""


class Player(object):

    def __init__(self):
        global money
        global health
        global current_shovel
        global current_pickaxe
        global current_axe
        global current_sword
        pass  # health, money, current tools/armor, farms, inventory,

    # Calculates the health taken vs current armor
    def defense(object, x):
        global current_helmet
        global current_chestplate
        global current_leggings
        global current_boots

        # x/0 is for calculating and taking armor durability
        # x/1 is for printing the armor bar
        numbers = [current_helmet[4], current_chestplate[4],
                   current_leggings[4], current_boots[4]]
        defense_average = sum(numbers) / len(numbers)

        if x > 0:
            if current_helmet[0] != 'skin':
                current_helmet[1] -= 1
                if current_helmet[1] == 0:
                    alert("Your helmet has broken")
                    current_helmet = ['skin', -1, 0, -1, 1]

            if current_chestplate[0] != 'skin':
                current_chestplate[1] -= 1
                if current_chestplate[1] == 0:
                    alert("Your chestplate has broken")
                    current_chestplate = ['skin', -1, 0, -1, 1]

            if current_leggings[0] != 'skin':
                current_leggings[1] -= 1
                if current_leggings[1] == 0:
                    alert("Your leggings have broken", 0)
                    current_leggings = ['skin', -1, 0, -1, 1]

            if current_boots[0] != 'skin':
                current_boots[1] -= 1
                if current_boots[1] == 0:
                    alert("Your boots have broken", 0)
                    current_boots = ['skin', -1, 0, -1, 1]

            return (math.ceil(x / defense_average))
        else:
            if defense_average > 1:
                return round((defense_average)*3)
            else:
                return 0

    # Calculates damage of sword + wolves
    def damage(object):
        global current_sword
        global wolves
        pain = 1
        if wolves > 0:
            pain = random.randint(1, 3) * current_sword[4]
            pain += wolves

            if current_sword[0] != 'fist':
                current_sword[1] -= 1
                if current_sword[1] == 0:
                    alert("Your sword has broken")
                    current_sword = ['fist', -1, 0, -1, .5]
            return pain

        else:
            pain = random.randint(1, 3) * current_sword[4]
            if current_sword[0] != 'fist':
                current_sword[1] -= 1
                if current_sword[1] == 0:
                    alert("Your sword has broken")
                    current_sword = ['fist', -1, 0, -1, .5]
            return pain
            pass  # returns pain(total damage done)


# [0name, 1health, 2msg, 3drop, 4extra_drop]
class Zombie(object):
    def __init__(self):
        self.health = 20
        self.msg = "The zombie bites you!\n"
        self.drop = 'rotten_flesh'
        self.name = 'zombie'

    def stats(self):
        self.mob = []
        self.mob.append(self.name)
        self.mob.append(self.health)
        self.mob.append(self.msg)
        self.mob.append(self.drop)
        return self.mob


class Skeleton(object):
    def __init__(self):
        self.health = 20
        self.msg = "The skeleton shoots you!\n"
        self.drop = 'bone'
        self.name = 'skeleton'

    def stats(self):
        self.mob = []
        self.mob.append(self.name)
        self.mob.append(self.health)
        self.mob.append(self.msg)
        self.mob.append(self.drop)
        return self.mob


class Witch(object):
    def __init__(self):
        self.health = 26
        self.msg = "The witch throws a damage potion at you!\n"
        self.msg2 = "The witch heals itself with a potion"
        self.drop = 'redstone'
        self.name = 'witch'

    def stats(self):
        self.mob = []
        self.mob.append(self.name)
        self.mob.append(self.health)
        self.mob.append(self.msg)
        self.mob.append(self.drop)
        self.mob.append(self.msg2)
        return self.mob


class Slime(object):
    def __init__(self):
        self.health = 16
        self.msg = "The slime stomps on you!\n"
        self.drop = 'slimeball'
        self.name = 'slime'

    def stats(self):
        self.mob = []
        self.mob.append(self.name)
        self.mob.append(self.health)
        self.mob.append(self.msg)
        self.mob.append(self.drop)
        return self.mob


class Creeper(object):
    def __init__(self):
        self.health = 20
        self.msg = "The creeper blows up!\n"
        self.drop = 'gunpowder'
        self.name = 'creeper'

    def stats(self):
        self.mob = []
        self.mob.append(self.name)
        self.mob.append(self.health)
        self.mob.append(self.msg)
        self.mob.append(self.drop)
        return self.mob


class Spider(object):
    def __init__(self):
        self.health = 16
        self.msg = "The spider bites you!\n"
        self.drop = 'string'
        self.name = 'spider'

    def stats(self):
        self.mob = []
        self.mob.append(self.name)
        self.mob.append(self.health)
        self.mob.append(self.msg)
        self.mob.append(self.drop)
        return self.mob


class Death(Screen):
    def __init__(self, **kwargs):
        super(Death, self).__init__(**kwargs)
        global death_message
        self.label = Label(
            font_size='50dp',
            size_hint=(None, None),
            height=int(Window.height)/6,
            width=int(Window.width)/2,
            pos_hint={'center_x': .5, 'center_y': .8}
        )
        self.add_widget(self.label)
        if death_message:
            self.label.text = death_message

        self.label2 = Label(
            text = 'You died...',
            font_size='50dp',
            size_hint=(None, None),
            height=int(Window.height)/6,
            width=int(Window.width)/2,
            pos_hint={'center_x': .5, 'center_y': .4}
        )
        self.add_widget(self.label2)

        self.btn = Button(
            text='Try again',
            font_size='50dp',
            size_hint=(None, None),
            height=int(Window.height)/6,
            width=int(Window.width)/2,
            pos_hint={'center_x': .5, 'center_y': .2}
        )
        self.btn.bind(on_press=self.restart)
        self.add_widget(self.btn)

    def restart(self, event):
        sm.switch_to(LoginScreen())


class ButtonColumn1(GridLayout):
    def __init__(self, **kwargs):
        super(ButtonColumn1, self).__init__(**kwargs)
        self.rows = 6

        self.btn1 = Button(
            text='Adventure',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0
        )
        self.btn1.bind(on_press=self.adventure)
        self.add_widget(self.btn1)

        self.btn2 = Button(
            text='Dig Down',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0
        )
        self.btn2.bind(on_press=self.dig_down)
        self.add_widget(self.btn2)

        self.btn3 = Button(
            text='Craft',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0
        )
        self.btn3.bind(on_press=self.craft)
        self.add_widget(self.btn3)

        self.btn4 = Button(
            text='Furnace',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0
        )
        self.btn4.bind(on_press=self.furnace)
        self.add_widget(self.btn4)

        self.btn5 = Button(
            text='Sleep',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0
        )
        self.btn5.bind(on_press=self.sleep)
        self.add_widget(self.btn5)

    def adventure(self, event):
        sm.switch_to(Adventure())

    def dig_down(self, event):
        sm.switch_to(DigDownScreen())

    def craft(self, event):
        sm.switch_to(Craft())

    def furnace(self, event):
        sm.switch_to(Furnace())

    def sleep(self, event):
        sm.switch_to(Sleep())


class ButtonColumn2(GridLayout):
    def __init__(self, **kwargs):
        super(ButtonColumn2, self).__init__(**kwargs)
        self.rows = 5

        self.btn1 = Button(
            text='Buildables',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0
        )
        self.btn1.bind(on_press=self.buildables)
        self.add_widget(self.btn1)

        self.btn2 = Button(
            text='Inventory',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0
        )
        self.btn2.bind(on_press=self.open_inventory)
        self.add_widget(self.btn2)

        self.btn3 = Button(
            text='Equipment',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0
        )
        self.btn3.bind(on_press=self.open_equipment)
        self.add_widget(self.btn3)

        self.btn4 = Button(
            text='Farm',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0
        )
        self.btn4.bind(on_press=self.farm)
        self.add_widget(self.btn4)

        self.btn5 = SettingsButton()
        self.btn5.font_size='40dp'
        self.btn5.height = int(Window.height)/8.0
        self.btn5.width = int(Window.width)/4.0
        #self.add_widget(self.btn5)


    def open_equipment(self, event):
        sm.switch_to(Equip())

    def open_inventory(self, event):
        sm.switch_to(Inv())

    def buildables(self, event):
        sm.switch_to(Buildables())

    def farm(self, event):
        sm.switch_to(FarmMenu())


class SettingsButton(Button):
    def __init__(self, **kwargs):
        super(SettingsButton, self).__init__(**kwargs)
        
        self = Builder.load_string('''Button:
    text: 'Settings'
    size_hint_x: None
    size_hint_y: None
    on_press: app.open_settings()''')


class MainLayout(RelativeLayout):
    global main_text

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        global money
        global night
        self.grid = GridLayout(cols=3)
        buttoncolumn1 = ButtonColumn1()
        buttoncolumn2 = ButtonColumn2()
        self.grid.add_widget(buttoncolumn1)
        self.label = Label(
            # Edit with global main_text = "x"
            text='',
            font_size='30dp',
            size_hint=(None, None),
            height=int(Window.height),
            width=int(Window.width)/2.0
        )
        self.day_label = Label(
            font_size='20dp',
            pos_hint={'center_x': .2, 'center_y': .2}
        )
        self.add_widget(self.day_label)
        if night:
            self.day_label.text = 'Crickets are chirping\nin the moonlight!'
        else:
            self.day_label.text = 'Birds are singing\nin the sunlight!'
        # health bar
        self.health = HealthBar(
            size_hint=(None, None),
            width=Window.width/2,
            height=Window.height/10
        )
        health_relative = RelativeLayout(
            size_hint=(None, None),
            pos_hint={'center_x': .5, 'center_y': .1}
        )
        health_relative.add_widget(self.health)
        self.add_widget(health_relative)
        # health bar
        money_label = Label(
            text='Money: $%s' % money,
            font_size='30dp',
            size_hint=(None, None),
            pos_hint={'center_x': .2, 'center_y': .06}
        )
        self.statbtn = Button(
            text='Stats',
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width)/4.0,
            pos_hint={'center_x': .5, 'center_y': .94}
        )
        self.statbtn.bind(on_press=self.stats)
        buttoncolumn2.add_widget(self.statbtn)

        self.add_widget(money_label)
        self.grid.add_widget(self.label)
        self.grid.add_widget(buttoncolumn2)
        self.add_widget(self.grid)

        Clock.schedule_once(self.on_start)

    def stats(self, event):
            sm.switch_to(Stats())

    def on_start(self, event):
        self.label.text = main_text
        # health bar
        # current equipment
        # farm notifications
        # day or night
        # etcetc


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        mainlayout = MainLayout()
        self.add_widget(mainlayout)        

    def on_enter(self):
        Clock.schedule_once(self.change_screen, 1)

    def change_screen(self, dt):
        if _just_exited_furnace:
            sm.switch_to(Furnace())
        else:
            pass
            # health bar
            # time of day
            # money in the bank


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.label = Label(
            text=splash,
            font_size='60dp',
            size_hint=(None, None),
            height=int(Window.height)/4,
            width=int(Window.width)/2,
            pos_hint={'center_x': .5, 'center_y': .7}
        )
        self.label2 = Label(
            text='Welcome, %s!'%user_id,
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/4,
            width=int(Window.width)/2,
            pos_hint={'center_x': .5, 'center_y': .5}
        )

        self.button = Button(
            text="Start",
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/5.0,
            width=int(Window.width)/3.0,
            pos_hint={'center_x': .25}
        )
        self.add_widget(self.label2)
        self.add_widget(self.label)
        self.button.bind(on_press=self.start)
        self.add_widget(self.button)

        self.btn2 = Button(
            text="Load Save",
            font_size='40dp',
            size_hint=(None, None),
            height=int(Window.height)/5.0,
            width=int(Window.width)/3.0,
            pos_hint={'center_x': .75}
        )
        self.add_widget(self.btn2)

    def start(self, event):
        sm.switch_to(MainScreen())


class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.label = Label(
            text='What is your username?',
            font_size='45dp',
            pos_hint={'center_x': .5, 'center_y': .85},
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width),
        )
        self.add_widget(self.label)

        self.input = TextInput(
            text='',
            font_size='45dp',
            size_hint=(None, None),
            height=int(Window.height)/8.0,
            width=int(Window.width),
            multiline=False,
            pos_hint={'center_x': .5, 'center_y': .65}
        )
        self.input.bind(on_text_validate=self.login)
        self.add_widget(self.input)

        self.btn = Button(
            text='Enter',
            font_size='35dp',
            size_hint=(None, None),
            height=int(Window.height)/5.0,
            width=int(Window.width),
            pos_hint={'center_x': .5}
        )
        self.btn.bind(on_press=self.login)
        self.add_widget(self.btn)

    def login(self, event):
        global user_id
        if self.input.text:
            user_id = self.input.text
        else:  # random username
            random_names = ['Saad Maan', 'Paul Ennis', 'Chris P. Bacon',
                            'Hand Majic', 'Don Duck', 'Mister Love',
                            'Ana Love', 'Pika Chew', 'Yoo Suk', 'Mike Oxlong']
            user_id = random_names[random.randint(0, len(random_names)-1)]

        sm.switch_to(WelcomeScreen())


class Buildables(Screen):
    def __init__(self, **kwargs):
        super(Buildables, self).__init__(**kwargs)
        
        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            size_hint_x=None,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )
        self.exitbtn.bind(on_press=self.go_home)
        self.add_widget(self.exitbtn)
        

    def go_home(self, event):
        sm.switch_to(MainScreen())


class Stats(Screen):
    def __init__(self, **kwargs):
        super(Stats, self).__init__(**kwargs)
        self.stat_grid = GridLayout()
        self.stat_scroll = ScrollView()
        self.achieve_grid = GridLayout()
        self.achieve_scroll = ScrollView()
        self.total_grid = GridLayout()
        self.total_scroll = ScrollView()
        dropdown = DropDown()

        btn1 = Button(text='animal', size_hint_y=None, height=int(Window.height)/9, font_size='45dp')
        btn1.bind(on_release=lambda btn: dropdown.select(btn1.text))
        btn1.bind(on_press=self.build_stat)
        dropdown.add_widget(btn1)

        btn2 = Button(text='ore', size_hint_y=None, height=int(Window.height)/9, font_size='45dp')
        btn2.bind(on_release=lambda btn: dropdown.select(btn2.text))
        btn2.bind(on_press=self.build_stat)
        dropdown.add_widget(btn2)

        btn3 = Button(text='tree', size_hint_y=None, height=int(Window.height)/9, font_size='45dp')
        btn3.bind(on_release=lambda btn: dropdown.select(btn3.text))
        btn3.bind(on_press=self.build_stat)
        dropdown.add_widget(btn3)

        btn4 = Button(text='craft', size_hint_y=None, height=int(Window.height)/9, font_size='45dp')
        btn4.bind(on_release=lambda btn: dropdown.select(btn4.text))
        btn4.bind(on_press=self.build_stat)
        dropdown.add_widget(btn4)

        btn5 = Button(text='cook', size_hint_y=None, height=int(Window.height)/9, font_size='45dp')
        btn5.bind(on_release=lambda btn: dropdown.select(btn5.text))
        btn5.bind(on_press=self.build_stat)
        dropdown.add_widget(btn5)

        btn6 = Button(text='harvest', size_hint_y=None, height=int(Window.height)/9, font_size='45dp')
        btn6.bind(on_release=lambda btn: dropdown.select(btn6.text))
        btn6.bind(on_press=self.build_stat)
        dropdown.add_widget(btn6)

        btn7 = Button(text='item', size_hint_y=None, height=int(Window.height)/9, font_size='45dp')
        btn7.bind(on_release=lambda btn: dropdown.select(btn7.text))
        btn7.bind(on_press=self.build_stat)
        dropdown.add_widget(btn7)

        btn8 = Button(text='misc', size_hint_y=None, height=int(Window.height)/9, font_size='45dp')
        btn8.bind(on_release=lambda btn: dropdown.select(btn8.text))
        btn8.bind(on_press=self.build_stat)
        dropdown.add_widget(btn8)

        mainbutton = Button(
                    text='Stats',
                    font_size='45dp',
                    size_hint=(None, None),
                    width=int(Window.width)/4,
                    height=int(Window.height)/9,
                    pos_hint={'center_x': .1, 'center_y': .94}
                )
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        self.add_widget(mainbutton)

        self.achievebtn = Button(
            text='Achievements',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/2,
            height=int(Window.height)/9,
            pos_hint={'center_x': .8, 'center_y': .94}
        )
        self.achievebtn.bind(on_press=self.achieve_btn_callback)
        self.add_widget(self.achievebtn)

        self.totalbtn = Button(
            text='Totals',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/9,
            pos_hint={'center_x': .39, 'center_y': .94}
        )
        self.totalbtn.bind(on_press=self.total_btn_callback)
        self.add_widget(self.totalbtn)

        self.exitbtn = Button(
            text='Exit',
            font_size='45dp',
            size_hint=(None, None),
            width=int(Window.width)/4,
            height=int(Window.height)/6,
            background_color=(0.77, 0.52, 1.24, 1),
            pos_hint={'center_x': .9, 'center_y': .1}
        )

        self.exitbtn.bind(on_press=self.exit)
        self.add_widget(self.exitbtn)

    def build_family_buttons(self):
        self.family_grid = GridLayout(rows=2)

    def build_stat(self, event):
        family = event.text
        self.remove_widget(self.stat_scroll)
        self.remove_widget(self.achieve_scroll)
        self.remove_widget(self.total_scroll)
        self.stat_scroll.clear_widgets()
        self.stat_scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height/2),
            pos_hint={'center_x': .5, 'center_y': .38},
            bar_color=([.81, .55, .55, 1]),  #
            bar_inactive_color=([.55, .17, .17, 1]))  #
        self.stat_grid.clear_widgets()
        self.stat_grid = GridLayout(
            size_hint=(None, 2),
            cols=1
        )
        x = 0
        for i in stats:
            if i[0] == family:
                live_stat = i[1]

        for i in range(int((len(live_stat))/2)):
            bstext = ('%s : %s') % (live_stat[x], live_stat[x+1])
            bstext = bstext.replace('_', ' ')
            btn = Button(
                text=bstext,
                font_size='45dp',
                disabled=True,
                size_hint=(None, None),
                width=int(Window.width)/1.1,
                height=int(Window.height)/9
            )
            self.stat_grid.add_widget(btn)
            x += 2
        
        self.stat_scroll.add_widget(self.stat_grid)
        self.add_widget(self.stat_scroll)
        self.remove_widget(self.exitbtn)
        self.add_widget(self.exitbtn)

    def achieve_btn_callback(self, event):

        self.remove_widget(self.stat_scroll)
        self.remove_widget(self.achieve_scroll)
        self.remove_widget(self.total_scroll)
        self.achieve_scroll.clear_widgets()
        self.achieve_scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height/2),
            pos_hint={'center_x': .5, 'center_y': .38},
            bar_color=([.81, .55, .55, 1]),  #
            bar_inactive_color=([.55, .17, .17, 1]))  #
        self.achieve_scroll.clear_widgets()
        self.achieve_grid = GridLayout(
            size_hint=(None, 2),
            cols=1
        )
        for i in achievements_list:
            if i[0] >= i[3]:
                bstext = ('"%s" for\n%s') % (i[2], i[4])
                self.btn = Button(
                    text = bstext,
                    font_size='45dp',
                    disabled=True,
                    size_hint=(None, None),
                    width=int(Window.width)/1.1,
                    height=int(Window.height)/3.5
                )
                self.achieve_grid.add_widget(self.btn)
        
        self.achieve_scroll.add_widget(self.achieve_grid)
        self.add_widget(self.achieve_scroll)
        self.remove_widget(self.exitbtn)
        self.add_widget(self.exitbtn)

    def total_btn_callback(self, event):
        self.remove_widget(self.stat_scroll)
        self.remove_widget(self.total_scroll)
        self.remove_widget(self.achieve_scroll)
        self.total_scroll.clear_widgets()
        self.total_scroll = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height/2),
            pos_hint={'center_x': .5, 'center_y': .38},
            bar_color=([.81, .55, .55, 1]),  #
            bar_inactive_color=([.55, .17, .17, 1]))  #
        self.total_scroll.clear_widgets()
        self.total_grid = GridLayout(
            size_hint=(None, 2),
            cols=1
        )
        
        self.btn1 = Button(
            text=str('%s animals killed' % sum(stats[0][1][1::2])),
            font_size='45dp',
            disabled=True,
            size_hint=(None, None),
            width=int(Window.width)/1.1,
            height=int(Window.height)/4.5
        )
        self.total_grid.add_widget(self.btn1)
        self.btn2 = Button(
            text=str('%s ores mined' % sum(stats[1][1][1::2])),
            font_size='45dp',
            disabled=True,
            size_hint=(None, None),
            width=int(Window.width)/1.1,
            height=int(Window.height)/4.5
        )
        self.total_grid.add_widget(self.btn2)

        x = 0
        var1 = 0
        var2 = 0
        for i in range(len(stats[2][1])):
            if stats[2][1][i] == 'trees':
                var1 = stats[2][1][i + 1]
            elif stats[2][1][i] == 'big_trees':
                var2 = stats[2][1][i + 1]
            x += 1
        self.btn3 = Button(
            text=str('%s trees chopped' % (var1 + var2)),
            font_size='45dp',
            disabled=True,
            size_hint=(None, None),
            width=int(Window.width)/1.1,
            height=int(Window.height)/4.5
        )
        self.total_grid.add_widget(self.btn3)
        self.btn4 = Button(
            text=str('%s Items crafted' % sum(stats[3][1][1::2])),
            font_size='45dp',
            disabled=True,
            size_hint=(None, None),
            width=int(Window.width)/1.1,
            height=int(Window.height)/4.5
        )
        self.total_grid.add_widget(self.btn4)
        self.btn5 = Button(
            text=str('%s items cooked' % sum(stats[4][1][1::2])),
            font_size='45dp',
            disabled=True,
            size_hint=(None, None),
            width=int(Window.width)/1.1,
            height=int(Window.height)/4.5
        )
        self.total_grid.add_widget(self.btn5)
        self.btn6 = Button(
            text=str('%s items harvested' % sum(stats[5][1][1::2])),
            font_size='45dp',
            disabled=True,
            size_hint=(None, None),
            width=int(Window.width)/1.1,
            height=int(Window.height)/4.5
        )
        self.total_grid.add_widget(self.btn6)
        self.btn7 = Button(
            text=str('%s items obtained' % sum(stats[6][1][1::2])),
            font_size='45dp',
            disabled=True,
            size_hint=(None, None),
            width=int(Window.width)/1.1,
            height=int(Window.height)/4.5
        )
        self.total_grid.add_widget(self.btn7)
        self.total_scroll.add_widget(self.total_grid)
        self.add_widget(self.total_scroll)
        self.remove_widget(self.exitbtn)
        self.add_widget(self.exitbtn)

    def exit(self, event):
        sm.switch_to(MainScreen())


class Testing(Screen):
    def __init__(self, **kwargs):
        super(Testing, self).__init__(**kwargs)
        Clock.schedule_once(self.testbtn)
        self.grid = GridLayout(cols=1)

        self.btn = Button(text='admin', font_size='30dp')
        self.btn.bind(on_press=self.admin)
        self.grid.add_widget(self.btn)

        self.btn1 = Button(text='login', font_size='30dp')
        self.btn1.bind(on_press=self.login)
        self.grid.add_widget(self.btn1)

        self.btn2 = Button(text='welcome', font_size='30dp')
        self.btn2.bind(on_press=self.welcome)
        self.grid.add_widget(self.btn2)

        self.btn3 = Button(text='villager', font_size='30dp')
        self.btn3.bind(on_press=self.villager)
        self.grid.add_widget(self.btn3)

        self.btn4 = Button(text='farm', font_size='30dp')
        self.btn4.bind(on_press=self.farm)
        self.grid.add_widget(self.btn4)

        self.btn5 = Button(text='equipment', font_size='30dp')
        self.btn5.bind(on_press=self.equip)
        self.grid.add_widget(self.btn5)

        self.btn6 = Button(text='inventory', font_size='30dp')
        self.btn6.bind(on_press=self.inventory)
        self.grid.add_widget(self.btn6)

        self.btn7 = Button(text='furnace', font_size='30dp')
        self.btn7.bind(on_press=self.furnace)
        self.grid.add_widget(self.btn7)

        self.btn8 = Button(text='cave', font_size='30dp')
        self.btn8.bind(on_press=self.cave)
        self.grid.add_widget(self.btn8)

        self.btn9 = Button(text='craft', font_size='30dp')
        self.btn9.bind(on_press=self.craft)
        self.grid.add_widget(self.btn9)

        self.btn10 = Button(text='adventure', font_size='30dp')
        self.btn10.bind(on_press=self.adventure)
        self.grid.add_widget(self.btn10)

        self.btn11 = Button(text='mainscreen', font_size='30dp')
        self.btn11.bind(on_press=self.mainscreen)
        self.grid.add_widget(self.btn11)

        self.btn12 = Button(text='dig down', font_size='30dp')
        self.btn12.bind(on_press=self.digdown)
        self.grid.add_widget(self.btn12)

        self.btn13 = Button(text='sleep', font_size='30dp')
        self.btn13.bind(on_press=self.sleep)
        self.grid.add_widget(self.btn13)

        self.btn14 = Button(text='achieve', font_size='30dp')
        self.btn14.bind(on_press=self.achieve)
        self.grid.add_widget(self.btn14)

        self.btn15 = Button(text='print stats', font_size='30dp')
        self.btn15.bind(on_press=self.stats)
        self.grid.add_widget(self.btn15)

        self.add_widget(self.grid)
    
    def stats(self, event):
        x = 0
        for i in stats:
            print("")
            for j in i:
                print(j)
                x += 1
                if x == 4:
                    x = 0
                    print("")

    def admin(self, event):
        self.remove_widget(self.grid)
        self.grid3 = GridLayout(cols=3)

        self.abtn1 = Button(text='store', font_size='30dp')
        self.abtn1.bind(on_press=self.store)
        self.grid3.add_widget(self.abtn1)
        self.inp1_a = TextInput(multiline=False)
        self.grid3.add_widget(self.inp1_a)
        self.inp1_b = TextInput(multiline=False)
        self.grid3.add_widget(self.inp1_b)

        self.add_widget(self.grid3)

    def store(self, event):
        item = self.inp1_a.text
        quantity = int(self.inp1_b.text)
        engine.store(item, quantity)

    def farm(self, event):
        self.remove_widget(self.grid)
        self.grid2 = GridLayout(cols=1)
        self.fbtn1=(Button(text='destroy', font_size='40dp'))
        self.fbtn1.bind(on_press=self.destroy)
        self.grid2.add_widget(self.fbtn1)

        self.fbtn2=(Button(text='menu', font_size='40dp'))
        self.fbtn2.bind(on_press=self.menu)
        self.grid2.add_widget(self.fbtn2)

        self.fbtn3=(Button(text='water', font_size='40dp'))
        self.fbtn3.bind(on_press=self.water)
        self.grid2.add_widget(self.fbtn3)
        
        self.fbtn4=(Button(text='select', font_size='40dp'))
        self.fbtn4.bind(on_press=self.select)
        self.grid2.add_widget(self.fbtn4)

        self.fbtn5=(Button(text='build', font_size='40dp'))
        self.fbtn5.bind(on_press=self.build)
        self.grid2.add_widget(self.fbtn5)

        self.add_widget(self.grid2)

    def testbtn(self, dt):
        self.btntest = Button(
            text='test',
            size_hint=(None, None),
            height=Window.height/12,
            width=Window.width/12,
            pos_hint={'center_x': .9, 'center_y': .9}
        )
        self.btntest.bind(on_press=testbtn_callback)
        Window.add_widget(self.btntest)

    def login(self, event):
        sm.switch_to(LoginScreen())

    def welcome(self, event):
        sm.switch_to(WelcomeScreen())

    def villager(self, event):
        sm.switch_to(VillagerScreen())

    def select(self, event):
        sm.switch_to(SelectFarm())

    def build(self, event):
        sm.switch_to(BuildFarm())

    def water(self, event):
        sm.switch_to(WaterFarm())

    def menu(self, event):
        sm.switch_to(FarmMenu())

    def destroy(self, event):
        sm.switch_to(DestroyFarm())

    def equip(self, event):
        sm.switch_to(Equip())

    def inventory(self, event):
        sm.switch_to(Inv())

    def furnace(self, event):
        sm.switch_to(Furnace())

    def cave(self, event):
        sm.switch_to(CaveScreen())

    def craft(self, event):
        sm.switch_to(Craft())

    def adventure(self, event):
        sm.switch_to(Adventure())

    def mainscreen(self, event):
        sm.switch_to(MainScreen())

    def digdown(self, event):
        sm.switch_to(DigDownScreen())

    def sleep(self, event):
        sm.switch_to(Sleep())

    def achieve(self, event):
        sm.switch_to(Achieved())   


player = Player()
engine = Engine()
stat = Stat()


class TextApp(App):

    def __init__(self, **kwargs):
        super(TextApp, self).__init__(**kwargs)
        self.config = ConfigParser()
        self.config.read('myconfig.ini')

    def build(self):
        # self.use_kivy_settings = False  # change later?
        # if fist_farm_build, call farm engine start
        Clock.schedule_once(
            self.start_farm_engine, 1
        )
        if testing:
            sm.add_widget(Testing(name='test'))
        if user_id == 'user_id':
            sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(WelcomeScreen(name='welcome'))  # test position
        sm.add_widget(IrrigateFarm(name='irrigate'))
        sm.add_widget(Stats(name='stats'))
        sm.add_widget(VillagerScreen(name='villager'))
        sm.add_widget(DestroyFarm(name='destroyfarm'))
        sm.add_widget(FarmMenu(name='farming'))
        sm.add_widget(WaterFarm(name='waterfarm'))
        sm.add_widget(SelectFarm(name='selectfarm'))
        sm.add_widget(BuildFarm(name='buildfarm'))
        sm.add_widget(Equip(name='equipment'))
        sm.add_widget(Inv(name='inventory'))
        sm.add_widget(Furnace(name='furnace'))
        sm.add_widget(CaveScreen(name='cave'))
        sm.add_widget(Craft(name='crafting'))
        sm.add_widget(Adventure(name='adventure'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(DigDownScreen(name='dig_down'))
        sm.add_widget(Sleep(name='sleep'))
        sm.add_widget(Buildables(name='buildables'))
        return sm

    def start_farm_engine(self, dt):
        if farming_started:
            Clock.schedule_interval(FarmEngine.interval, 10)
        if is_cooking:
            Clock.schedule_interval(engine.count_down, 1)

    # The fuck is this?
    def callback(self):
            global _just_exited_furnace
            if _just_exited_furnace == True:
                sm.switch_to(Furnace())

    def on_stop(self):
        engine = Engine()
        engine.save()
    
    def on_pause(self):
        engine = Engine()
        engine.save()
        return True

    def build_config(self, config):
        config.setdefaults("example", {
            'boolexample': True
        })
        config.setdefaults("graphics", {
            'fullscreen': True
        })

    def build_settings(self, settings):
        # settings.add_json_panel('My custon panel',
        # self.config,
        # data=json_settings)
        pass

    def on_config_change(self, config, section, key, value):
        if key == "upper_num":
            self.root.math_screen.max_num = int(value)

        elif key == "lower_num":
            self.root.math_screen.min_num = int(value)


def userdata():
    global inventory
    global all_farms
    global base
    global equipment
    global achievements_list
    global stats
    inventory = copy.deepcopy(
            store_file.get('inventory')['content'])
    all_farms = copy.deepcopy(
        store_file.get('all_farms')['content'])
    base = copy.deepcopy(
        store_file.get('base')['content'])
    equipment = copy.deepcopy(
        store_file.get('equipment')['content'])
    achievements_list = copy.deepcopy(
        store_file.get('achievements_list')['content'])
    stats = copy.deepcopy(
        store_file.get('stats')['content'])

if True:
    global inventory
    global all_farms
    global base
    global equipment
    global achievements_list
    global stats
    global _just_exited_furnace
    textapp = TextApp()
    Craft.scroll_pos = 1
    Craft.menu = 'main'
    Craft.menu_scroll_pos = 1
    Inv.scroll_pos = 1
    _just_exited_furnace = False
    selected_farm = None
    xvbbb = -300
    xxz = -300
    death_message = 'You Died'
    farmx_label = Label(
        text='A farm is ready to harvest',
        font_size='60dp'
    )
    alertx_label = Label(
        font_size='60dp'
    )
    # Simply, lists
    if True:

        # TOOLS LISTS
        if True:  # ['wooden_pickaxe', 59, 1, 59, 1],
            # type, current durability, power, total durability
            # type, current durability, defense, total durability
            tools = [
                ['gold_pickaxe', 32, 2, 32, 4],
                ['wooden_pickaxe', 59, 1, 59, 1],
                ['stone_pickaxe', 131, 2, 131, 2],
                ['iron_pickaxe', 250, 3, 250, 3],
                ['diamond_pickaxe', 1561, 4, 1561, 4],
                ['gold_axe', 32, 2, 32, 4],
                ['wooden_axe', 59, 1, 59, 1],
                ['stone_axe', 131, 2, 131, 2],
                ['iron_axe', 250, 3, 250, 3],
                ['diamond_axe', 1561, 4, 1561, 4],
                ['gold_shovel', 32, 2, 32, 4],
                ['wooden_shovel', 59, 1, 59, 1],
                ['stone_shovel', 131, 2, 131, 2],
                ['iron_shovel', 250, 3, 250, 3],
                ['diamond_shovel', 1561, 4, 1561, 4],
                ['gold_sword', 32, 2, 32, 3],
                ['wooden_sword', 59, 1, 59, 1],
                ['stone_sword', 131, 2, 131, 2],
                ['iron_sword', 250, 3, 250, 3],
                ['diamond_sword', 1561, 4, 1561, 4],
                ['log_helmet', 56, 2, 56, 2],
                ['log_chestplate', 81, 1, 81, 2],
                ['log_leggings', 76, 2, 76, 2],
                ['log_boots', 66, 4, 66, 2],
                ['iron_helmet', 166, 2, 166, 3],
                ['iron_chestplate', 241, 1, 241, 3],
                ['iron_leggings', 226, 2, 226, 3],
                ['iron_boots', 196, 4, 196, 3],
                ['gold_helmet', 78, 2, 78, 3],
                ['gold_chestplate', 113, 1, 113, 3],
                ['gold_leggings', 106, 2, 106, 3],
                ['gold_boots', 92, 4, 92, 3],
                ['diamond_helmet', 364, 2, 364, 4],
                ['diamond_chestplate', 529, 1, 529, 4],
                ['diamond_leggings', 496, 2, 496, 4],
                ['diamond_boots', 430, 4, 430, 4],
                ['bedrock_helmet', 921, 2, 921, 5],
                ['bedrock_chestplate', 1338, 1, 1338, 5],
                ['bedrock_leggings', 1254, 2, 1254, 5],
                ['bedrock_boots', 1087, 4, 1087, 5],
                ['lapis_helmet', 56, 2, 56, 2],
                ['lapis_chestplate', 81, 1, 81, 2],
                ['lapis_leggings', 76, 2, 76, 2],
                ['lapis_boots', 66, 4, 66, 2]
            ]

            picks = ['gold_pickaxe', 'wooden_pickaxe', 'stone_pickaxe',
                     'iron_pickaxe', 'diamond_pickaxe']

            shovels = ['gold_shovel', 'wooden_shovel', 'stone_shovel',
                       'iron_shovel', 'diamond_shovel']

            axes = ['gold_axe', 'wooden_axe', 'stone_axe',
                    'iron_axe', 'diamond_axe']

            swords = ['gold_sword', 'wooden_sword', 'stone_sword',
                      'iron_sword', 'diamond_sword']

            helmets = ['log_helmet', 'iron_helmet', 'gold_helmet',
                       'diamond_helmet', 'bedrock_helmet', 'lapis_helmet']

            chestplates = ['log_chestplate', 'iron_chestplate',
                           'gold_chestplate', 'diamond_chestplate',
                           'bedrock_chestplate', 'lapis_chestplate']

            leggings = ['log_leggings', 'iron_leggings',
                        'gold_leggings', 'diamond_leggings',
                        'bedrock_leggings', 'lapis_leggings']

            boots = ['log_boots', 'iron_boots',
                     'gold_boots', 'diamond_boots',
                     'bedrock_boots', 'lapis_boots']

        # FARM LISTS
        if True:
            farm_materials = [
                ['log', 50000],  # 1% every hour
                ['stone', 20000],  # .4% every hour
                ['iron_block', 5000],  # .1% every hour
                ['gold_block', 3500],  # .07% every hour
                ['diamond_block', 2000],  # .04% every hour
                ['obsidian', 1000],  # .02% every hour
                ['bedrock', 10]  # %>0 every hour
            ]

            CropFarmType = [
                ['cocoa', 250],
                ['wheat', 500],
                ['log', 1000]
            ]

            AnimalFarmType = [
                ['pig', 600],
                ['cow', 1350]
            ]

            MonsterFarmType = [
                ['skeleton', 10000]
            ]
            allfarmtype = ['cocoa', 'wheat', 'log',
                           'pig', 'cow', 'skeleton']

        # MISC LISTS
        if True:

            witch_drops = ['redstone', 'glowstone', 'diamond']

            fishing_items = ['leather', 'seaweed', 'bone', 'reed',
                             'sitck', 'dirt'
            ]
            edible = [
                ['raw_porkchop', 5], ['raw_beef', 5],
                ['cooked_porkchop', 20], ['cooked_beef', 20],
                ['apple', 8], ['rotten_flesh', 3], ['raw_fish', 5],
                ['cooked_fish', 15], ['cooked_chicken', 20],
                ['cooked_lambchop', 20], ['raw_chicken', 5],
                ['raw_lambchop', 5], ['bread', 20]
            ]
            edible2 = ['raw_porkchop', 'raw_beef',
                'cooked_porkchop', 'cooked_beef',
                'apple', 'rotten_flesh', 'raw_fish',
                'cooked_fish', 'cooked_chicken',
                'cooked_lambchop', 'raw_chicken',
                'raw_lambchop', 'bread']
            semi_edible = [
                'raw_porkchop', 'raw_beef', 'raw_fish', 'raw_chicken',
                'raw_lambchop', 'rotten_flesh'
            ]

            animal = ['wolf', 'chicken', 'chicken', 'chicken',
                      'pig', 'pig', 'pig', 'cow',
                      'cow', 'cow', 'sheep', 'sheep', 'sheep']

            animal_night = [
                'wolf', 'chicken', 'pig', 'cow', 'sheep',
                'zombie', 'zombie', 'skeleton', 'skeleton',
                'witch', 'slime', 'creeper', 'spider',
                'zombie', 'zombie', 'skeleton', 'skeleton',
                'witch', 'slime', 'creeper', 'spider'
            ]

            friend = ['chicken', 'pig', 'cow', 'sheep']
            foe = ['zombie', 'skeleton', 'witch', 'spider', 'slime', 'creeper']

            # ['', ##, (0 for none, 1 for wood pick, 2 for stone pick, ...
            # 3 for iron pick, 4 for diamond_pick, 5 is unbreakable)]
            ores = [
                ['bedrock', 5, 5], ['diamond', 14, 3], ['redstone', 14, 3],
                ['gold_ore', 30, 3], ['lapis', 30, 3], ['lava', 30],
                ['iron_ore', 61, 2], ['coal', 61, 1], ['gravel', 61, 0],
                ['cobblestone', 61, 1], ['dirt', 0, 0], ['obsidian', 0, 4]
            ]

            cave_ores = [
                ['diamond', 14, 3], ['redstone', 14, 3],
                ['gold_ore', 30, 3], ['lapis', 30, 3],
                ['iron_ore', 61, 2], ['coal', 61, 1]
            ]

            prices = [
                ['log', 1], ['cobble', 2], ['gravel', 2],
                ['diamond', 20], ['apple', 10],
                ['iron', 5], ['leather', 5], ['redstone', 5],
                ['obsidian', 20], ['stone', 3],
                ['bedrock', 340], ['cocoa', 3], ['lapis', 15],
                ['gold', 10], ['dirt', 1], ['bread', 10]
            ]

        # CRAFTING LIST
        if True:

            # for 1 material [item to craft,
                            # material,
                            # quantity of material,
                            # quantity received]
            # for 2 material [item to craft,
                            # material,
                            # quantity of material,
                            # material2,
                            # quantity of material2,
                            # quantity received]
            crafting = [
                ['wool', 'string', 4, 1],
                ['furnace', 'cobblestone', 8, 1],
                ['bed', 'wool', 3, 'wood_plank', 3, 1],
                ['wood_plank', 'log', 1, 4],
                ['stick', 'wood_plank', 2, 4],
                ['fishing_rod', 'stick', 3, 'string', 2, 1],
                ['bucket', 'iron', 3, 1],
                ['torch', 'coal', 1, 'stick', 1, 4],
                ['crafting_table', 'wood_plank', 4, 1],
                ['gold_pickaxe', 'stick', 2, 'gold', 3, 1],
                ['wooden_pickaxe', 'stick', 2, 'wood_plank', 3, 1],
                ['stone_pickaxe', 'stick', 2, 'cobblestone', 3, 1],
                ['iron_pickaxe', 'stick', 2, 'iron', 3, 1],
                ['diamond_pickaxe', 'stick', 2, 'diamond', 3, 1],
                ['bread', 'wheat', 3, 1],
                ['paper', 'sugar_cane', 3, 1],
                ['book', 'leather', 1, 'paper', 3, 1],
                ['book_shelf', 'wood_plank', 6, 'book', 3, 1],
                ['log_helmet', 'log', 5, 1],
                ['log_chestplate', 'log', 8, 1],
                ['log_leggings', 'log', 7, 1],
                ['log_boots', 'log', 4, 1],
                ['iron_helmet', 'iron', 5, 1],
                ['iron_chestplate', 'iron', 8, 1],
                ['iron_leggings', 'iron', 7, 1],
                ['iron_boots', 'iron', 4, 1],
                ['gold_helmet', 'gold', 5, 1],
                ['gold_chestplate', 'gold', 8, 1],
                ['gold_leggings', 'gold', 7, 1],
                ['gold_boots', 'gold', 4, 1],
                ['diamond_helmet', 'diamond', 5, 1],
                ['diamond_chestplate', 'diamond', 8, 1],
                ['diamond_leggings', 'diamond', 7, 1],
                ['diamond_boots', 'diamond', 4, 1],
                ['bedrock_helmet', 'bedrock', 5, 1],
                ['bedrock_chestplate', 'bedrock', 8, 1],
                ['bedrock_leggings', 'bedrock', 7, 1],
                ['bedrock_boots', 'bedrock', 4, 1],
                ['lapis_helmet', 'lapis', 5, 1],
                ['lapis_chestplate', 'lapis', 8, 1],
                ['lapis_leggings', 'lapis', 7, 1],
                ['lapis_boots', 'lapis', 4, 1],
                ['gold_axe', 'stick', 2, 'gold', 3, 1],
                ['wooden_axe', 'stick', 2, 'wood_plank', 3, 1],
                ['stone_axe', 'stick', 2, 'cobblestone', 3, 1],
                ['iron_axe', 'stick', 2, 'iron', 3, 1],
                ['diamond_axe', 'stick', 2, 'diamond', 3, 1],
                ['gold_shovel', 'stick', 2, 'gold', 1, 1],
                ['wooden_shovel', 'stick', 2, 'wood_plank', 1, 1],
                ['stone_shovel', 'stick', 2, 'cobblestone', 1, 1],
                ['iron_shovel', 'stick', 2, 'iron', 1, 1],
                ['diamond_shovel', 'stick', 2, 'diamond', 1, 1],
                ['gold_sword', 'stick', 1, 'gold', 2, 1],
                ['wooden_sword', 'stick', 1, 'wood_plank', 2, 1],
                ['stone_sword', 'stick', 1, 'cobblestone', 2, 1],
                ['iron_sword', 'stick', 1, 'iron', 2, 1],
                ['diamond_sword', 'stick', 1, 'diamond', 2, 1],
                ['coal_block', 'coal', 9, 1],
                ['iron_block', 'iron', 9, 1],
                ['gold_block', 'gold', 9, 1],
                ['diamond_block', 'diamond', 9, 1],
                ['redstone_block', 'redstone', 9, 1],
                ['coal', 'coal_block', 1, 9],
                ['iron', 'iron_block', 1, 9],
                ['gold', 'gold_block', 1, 9],
                ['diamond', 'diamond_block', 1, 9],
                ['redstone', 'redstone_block', 1, 9],
                ['bedrock', 'diamond_block', 1, 'obsidian', 8, 1],
                ['watch', 'gold', 4, 'redstone', 1, 1],
                ['compass', 'iron', 4, 'redstone', 1, 1],
                ['dynamite', 'gunpowder', 5, 'sand', 4, 1]
            ]
            crafting.sort()

            armor_type = ['bedrock_boots',
            'bedrock_chestplate',
            'bedrock_helmet',
            'bedrock_leggings',
            'diamond_boots',
            'diamond_chestplate',
            'diamond_helmet',
            'diamond_leggings',
            'iron_boots',
            'iron_chestplate',
            'iron_helmet',
            'iron_leggings',
            'lapis_boots',
            'lapis_chestplate',
            'lapis_helmet',
            'lapis_leggings',
            'log_boots',
            'log_chestplate',
            'log_helmet',
            'log_leggings',
            'gold_boots',
            'gold_chestplate',
            'gold_helmet',
            'gold_leggings',]

            tool_type = ['diamond_axe',
            'diamond_pickaxe',
            'diamond_shovel',
            'diamond_sword',
            'iron_axe',
            'iron_pickaxe',
            'iron_shovel',
            'iron_sword',
            'gold_axe',
            'gold_pickaxe',
            'gold_shovel',
            'gold_sword',
            'wooden_axe',
            'wooden_pickaxe',
            'wooden_shovel',
            'wooden_sword',
            'stone_axe',
            'stone_pickaxe',
            'stone_shovel',
            'stone_sword',]

            block_type = ['bedrock',
            'diamond_block',
            'iron_block',
            'gold_block',
            'coal',
            'coal_block',
            'diamond',
            'gold',
            'redstone',
            'redstone_block',
            'iron',]

            misc_type = ['wood_plank',
            'stick',
            'book',
            'bed',
            'book_shelf',
            'bread',
            'bucket',
            'compass',
            'crafting_table',
            'dynamite',
            'fishing_rod',
            'furnace',
            'paper',
            'torch',
            'watch']

        # FURNACE LISTS
        if True:
            fuel_quantity = [
                ['coal', 8],
                ['log', 4],
                ['wood_plank', 2],
                ['stick', 1],
                ['wooden_pickaxe', 3],
                ['wooden_shovel', 2],
                ['wooden_axe', 3],
                ['wooden_sword', 3],
                ['log_helmet', 10],
                ['log_chestplate', 16],
                ['log_leggings', 14],
                ['log_boots', 8],
                ['coal_block', 72]
            ]
            fuel_quantity.sort()

            cook_output = [
                ['iron_ore', 'iron'],
                ['raw_porkchop', 'cooked_porkchop'],
                ['raw_beef', 'cooked_beef'],
                ['gold_ore', 'gold'],
                ['cobblestone', 'stone'],
                ['log', 'coal'],
                ['raw_fish', 'cooked_fish'],
                ['raw_lambchop', 'cooked_lambchop'],
                ['raw_chicken', 'cooked_chicken'],
                ['sand', 'glass']
            ]
            cook_output.sort()


    # Importing save file 'textcraft'
    # Collecting global v ariables
    data_dir = (textapp.user_data_dir)
    store_file = JsonStore(join(data_dir, 'textcraft.json'))
    # store_file = JsonStore('textcraft.json')

    if store_file.exists('inventory'):
        userdata()

    else:
        # [variable ,Don't have have 0 or 1 ,goal ,
        # "achievement",reason for achievement]
        achievements_list = [
            [0, 0, 'Dirt Miner', 100, 'mining 100 dirt'],  # 0
            [0, 0, 'Dirty Diamonds', 2, 'mining 2 diamonds'],  # 1
            [0, 0, 'Tree Hugger(not)', 50, 'killing 50 trees'],  # 2
            [0, 0, 'Cover Me Feet', 1, 'pouring water on lava (not dying)'],
            [0, 0, 'Sorry, Mom', 1, 'killing a cow'],  # 4
            [0, 0, 'Jill', 20, 'filling your bucket 20 times'],  # 5
            [0, 0, 'Good morning, ladies', 10, 'catching 10 fish'],  # 6
            [0, 0, 'Bitch Tamer', 5, 'taming 5 wolves'],  # 7
            [0, 0, 'Dar3 D3vil', 10, 'killing 10 creepers'],  # 8
            [0, 0, 'Worrisome', 100, 'opening inventory 100 times'],  # 9
            [0, 0, 'Oink, Oink', 100, 'eat 100 items']  # 10
            # 11 millionaire
        ]
        current_time = (math.floor(time.time()))
        inventory = [['torch', 1]]
        all_farms = []
        base = [0, 0, 100, 0, 0, 0,
            ['fist',-1, 0, -1, .5], 'user_id',
            ['fist', -1, 0, -1, .5],
            ['fist', -1, 0, -1, .5],
            ['skin', -1, 0, -1, 1],
            ['skin', -1, 0, -1, 1],
            ['skin', -1, 0, -1, 1],
            ['skin', -1, 0, -1, 1],
            ['fist', -1, 0, -1, .5],
            current_time, 1, 0, False, False, 0, []]
        equipment = []

        stats = [['animal', []],
                ['ore', []],
                ['tree',[]],
                ['craft', []],
                ['cook', []],
                ['harvest', []],
                ['item', []],
                ['misc', []]]

    height = 64
    night = base[0]
    furnace_have = base[1]
    health = base[2]
    wolves = base[3]
    clock = base[4]
    money = base[5]
    current_pickaxe = base[6]
    user_id = base[7]
    current_shovel = base[8]
    current_axe = base[9]
    current_helmet = base[10]
    current_chestplate = base[11]
    current_leggings = base[12]
    current_boots = base[13]
    current_sword = base[14]
    current_time = base[15]
    furnace_level = base[16]
    time_left_cooking = base[17]
    is_cooking = base[18]
    farming_started = base[19]
    time_passed_storm = base[20]
    cooking_chart = base[21]



if __name__ ==('__main__'):
    TextApp().run()
    # except Exception as e:

# end