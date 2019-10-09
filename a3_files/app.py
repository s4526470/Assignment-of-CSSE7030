"""
Simple 2d world where the player can interact with the items in the world.
"""

__author__ = ""
__date__ = ""
__version__ = "1.1.0"
__copyright__ = "The University of Queensland, 2019"

import tkinter as tk
import random
from collections import namedtuple
import tkinter.messagebox
import pymunk


from block import Block, ResourceBlock, BREAK_TABLES, LeafBlock, TrickCandleFlameBlock
from grid import Stack, Grid, SelectableGrid, ItemGridView
from item import Item, SimpleItem, HandItem, BlockItem, MATERIAL_TOOL_TYPES, TOOL_DURABILITIES
from player import Player
from dropped_item import DroppedItem
from crafting import GridCrafter, CraftingWindow,GridCrafterView
from world import World
from core import positions_in_range
from game import GameView, WorldViewRouter
from mob import Bird, Mob

BLOCK_SIZE = 2 ** 5
GRID_WIDTH = 2 ** 5
GRID_HEIGHT = 2 ** 4

# Task 3/Post-grad only:
# Class to hold game data that is passed to each thing's step function
# Normally, this class would be defined in a separate file
# so that type hinting could be used on PhysicalThing & its
# subclasses, but since it will likely need to be extended
# for these tasks, we have defined it here
GameData = namedtuple('GameData', ['world', 'player'])


def create_block(*block_id):
    """(Block) Creates a block (this function can be thought of as a block factory)

    Parameters:
        block_id (*tuple): N-length tuple to uniquely identify the block,
        often comprised of strings, but not necessarily (arguments are grouped
        into a single tuple)

    Examples:
        >>> create_block("leaf")
        LeafBlock()
        >>> create_block("stone")
        ResourceBlock('stone')
        >>> create_block("mayhem", 1)
        TrickCandleFlameBlock(1)
    """
    if len(block_id) == 1:
        block_id = block_id[0]
        if block_id == "leaf":
            return LeafBlock()
        elif block_id in BREAK_TABLES:
            return ResourceBlock(block_id, BREAK_TABLES[block_id])

    elif block_id[0] == 'mayhem':
        return TrickCandleFlameBlock(block_id[1])
    
    

    raise KeyError(f"No block defined for {block_id}")


def create_item(*item_id):
    """(Item) Creates an item (this function can be thought of as a item factory)

    Parameters:
        item_id (*tuple): N-length tuple to uniquely identify the item,
        often comprised of strings, but not necessarily (arguments are grouped
        into a single tuple)

    Examples:
        >>> create_item("dirt")
        BlockItem('dirt')
        >>> create_item("hands")
        HandItem('hands')
        >>> create_item("pickaxe", "stone")  # *without* Task 2.1.2 implemented
        Traceback (most recent call last):
        ...
        NotImplementedError: "Tool creation is not yet handled"
        >>> create_item("pickaxe", "stone")  # *with* Task 2.1.2 implemented
        ToolItem('stone_pickaxe')
    """
    if len(item_id) == 2:
        
        if item_id[0] in MATERIAL_TOOL_TYPES and item_id[1] in TOOL_DURABILITIES:
            return ToolItem("stone_pickaxe","axe", 1000) 
            raise NotImplementedError("Tool creation is not yet handled")
            
        
        

    elif len(item_id) == 1:

        item_type = item_id[0]

        if item_type == "hands":
            return HandItem("hands")

        elif item_type == "dirt":
            return BlockItem(item_type)
        
        elif item_type == "wood":
            return BlockItem(item_type)
        elif item_type == "stone":
            return BlockItem(item_type) 
        elif item_type == "apple":
            return FoodItem(item_type,2)
        elif item_type == "stick":
            return BlockItem(item_type)
        

    raise KeyError(f"No item defined for {item_id}")



class StatusView(tk.Frame) :
    """ status view frame """

    def __init__(self, master) :
        """
        Parameters:
            master(tk): windows in which this frame is to be drawn
        """
        super().__init__(master)
        self._health_label = tk.Label(self, text="Health: ")
        self._health_label.pack(side=tk.LEFT, padx=5)
        self._food_label = tk.Label(self, text="Food: ")
        self._food_label.pack(side=tk.LEFT)
    
    def set_health_value(self,new_health_value) :
        self._health_label.config(text="Health: " + str(new_health_value))
    def set_food_value(self, new_food_value) :
        self._food_label.config(text="Food: " + str(new_food_value))


BLOCK_COLOURS = {
    'diamond': 'blue',
    'dirt': '#552015',
    'stone': 'grey',
    'wood': '#723f1c',
    'leaves': 'green',
    'crafting_table': 'pink',
    'furnace': 'black',
}

ITEM_COLOURS = {
    'diamond': 'blue',
    'dirt': '#552015',
    'stone': 'grey',
    'wood': '#723f1c',
    'apple': '#ff0000',
    'leaves': 'green',
    'crafting_table': 'pink',
    'furnace': 'black',
    'cooked_apple': 'red4'
}


def load_simple_world(world):
    """Loads blocks into a world

    Parameters:
        world (World): The game world to load with blocks
    """
    block_weights = [
        (100, 'dirt'),
        (30, 'stone'),
    ]

    cells = {}

    ground = []

    width, height = world.get_grid_size()

    for x in range(width):
        for y in range(height):
            if x < 22:
                if y <= 8:
                    continue
            else:
                if x + y < 30:
                    continue

            ground.append((x, y))

    weights, blocks = zip(*block_weights)
    kinds = random.choices(blocks, weights=weights, k=len(ground))

    for cell, block_id in zip(ground, kinds):
        cells[cell] = create_block(block_id)

    trunks = [(3, 8), (3, 7), (3, 6), (3, 5)]

    for trunk in trunks:
        cells[trunk] = create_block('wood')

    leaves = [(4, 3), (3, 3), (2, 3), (4, 2), (3, 2), (2, 2), (4, 4), (3, 4), (2, 4)]

    for leaf in leaves:
        cells[leaf] = create_block('leaf')

    for cell, block in cells.items():
        # cell -> box
        i, j = cell

        world.add_block_to_grid(block, i, j)

    world.add_block_to_grid(create_block("mayhem", 0), 14, 8)

    world.add_mob(Bird("friendly_bird", (12, 12)), 400, 100)
    #world.add_mob(Sheep("friendly_bird", (12, 12)), 400, 100)


class Ninedraft:
    """High-level app class for Ninedraft, a 2d sandbox game"""

    def __init__(self, master):
        """Constructor

        Parameters:
            master (tk.Tk): tkinter root widget
        """

        self._master = master
        self._master.title("Ninedraft")
        self._world = World((GRID_WIDTH, GRID_HEIGHT), BLOCK_SIZE)

        load_simple_world(self._world)

        self._player = Player()
        self._world.add_player(self._player, 250, 150)

        self._world.add_collision_handler("player", "item", on_begin=self._handle_player_collide_item)

        self._hot_bar = SelectableGrid(rows=1, columns=10)
        self._hot_bar.select((0, 0))



        starting_hotbar = [
            Stack(create_item("dirt"), 20),
            Stack(create_item("pickaxe", "stone"), 1)
        ]

        for i, item in enumerate(starting_hotbar):
            self._hot_bar[0, i] = item

        self._hands = create_item("hands")
        self._weapon = create_item("pickaxe", "stone") 

        starting_inventory = [
            ((1, 5), Stack(Item('dirt'), 10)),
            ((0, 2), Stack(Item('wood'), 10)),
        ]
        self._inventory = Grid(rows=3, columns=10)
        for position, stack in starting_inventory:
            self._inventory[position] = stack

       
        

        self._crafting_window = None
        self._master.bind("e",
                          lambda e: self.run_effect(('crafting', 'basic')))

        self._view = GameView(master, self._world.get_pixel_size(), WorldViewRouter(BLOCK_COLOURS, ITEM_COLOURS))
        self._view.pack()

        

        self._master.bind("<Motion>", self._mouse_move)
        self._master.bind("<Button-1>", self._left_click)
        self._master.bind("<Button-2>", self._right_click)
        
        
        
        

        # Task 1.3: Create instance of StatusView here
        # ...

        self._status_view = StatusView(master) 
        self._status_view.pack()                             
        self._status_view.set_food_value(self._player.get_food())
        self._status_view.set_health_value(self._player.get_health())
        
        

        self._hot_bar_view = ItemGridView(master, self._hot_bar.get_size())
        self._hot_bar_view.pack(side=tk.TOP, fill=tk.X)





        self._master.bind("<space>", lambda e: self._jump()) #2019.5.22改
        self._master.bind("a", lambda e: self._move(-1, 0))
        self._master.bind("<Left>", lambda e: self._move(-1, 0))
        self._master.bind("d", lambda e: self._move(1, 0))
        self._master.bind("<Right>", lambda e: self._move(1, 0))
        self._master.bind("s", lambda e: self._move(0, 1))
        self._master.bind("<Down>", lambda e: self._move(0, 1))





       
        self._master.bind("1", lambda e: self._activate_item(0))
        self._master.bind("2", lambda e: self._activate_item(1))
        self._master.bind("3", lambda e: self._activate_item(2))
        self._master.bind("4", lambda e: self._activate_item(3))
        self._master.bind("5", lambda e: self._activate_item(4))
        self._master.bind("6", lambda e: self._activate_item(5))
        self._master.bind("7", lambda e: self._activate_item(6))
        self._master.bind("8", lambda e: self._activate_item(7))
        self._master.bind("9", lambda e: self._activate_item(8))
        self._master.bind("0", lambda e: self._activate_item(9))




        # Task 1.6 File Menu & Dialogs: Add file menu here
        # ...
        menu = MenuBar(master, [("File", {"New Game": self._reset,  
                                          "Exit": self._close})])
        
        

        self._target_in_range = False
        self._target_position = 0, 0
        

        self.redraw()

        self.step()
    def _reset(self) :
        self._master.destroy()
        main()
    def _close(self) :

        """ Exit the drawing application """
        result = tk.messagebox.askquestion(title="Quiz Window", message="Do you really wanna quiz?")
        if (result == "yes") :
            self._master.destroy()
        
        

        
        

    def redraw(self):
        self._view.delete(tk.ALL)

        # physical things
        self._view.draw_physical(self._world.get_all_things())

        # target
        target_x, target_y = self._target_position
        target = self._world.get_block(target_x, target_y)
        cursor_position = self._world.grid_to_xy_centre(*self._world.xy_to_grid(target_x, target_y))

        

        #2019.5.22
        if self._target_in_range : 
            self._target_position = cursor_position
             
            self._view.show_target(self._player.get_position(),self._target_position, cursor_position) 
        else :
            self._view.hide_target()

 

        # Task 1.3 StatusView: Update StatusView values here
        # ...

        # hot bar
        self._hot_bar_view.render(self._hot_bar.items(), self._hot_bar.get_selected())

    def step(self):
        data = GameData(self._world, self._player)
        self._world.step(data)
        self.check_target()
        self.redraw()

        # Task 1.6 File Menu & Dialogs: Handle the player's death if necessary
        # ...
       

        self._master.after(15, self.step)

    def _move(self, dx, dy):
        velocity = self._player.get_velocity()
        self._player.set_velocity((velocity.x + dx * 80, velocity.y + dy * 80))

    def _jump(self):
        velocity = self._player.get_velocity()
        self._player.set_velocity((velocity.x + 10, velocity.y - 100)) 
        

    def mine_block(self, block, x, y):
        luck = random.random()

        active_item, effective_item = self.get_holding()

        was_item_suitable, was_attack_successful = block.mine(effective_item, active_item, luck)

        effective_item.attack(was_attack_successful)

        if block.is_mined():
            # Task 1.2 Mouse Controls: Reduce the player's food/health appropriately
            if self._player.get_food() > 0 :    
                self._player.change_health(0)
                self._player.change_food(-2)                                                       
                self._status_view.set_food_value(self._player.get_food())                         
                
            elif self._player.get_food() == 0 : 
                self._player.change_food(0) 
                self._player.change_health(-2)
                self._status_view.set_health_value(self._player.get_health())

            if self._player.is_dead() : 
                result = tk.messagebox.askquestion(title="You are dead!", message="Do you want to try again?")
                if (result == "yes") :
                    self._reset()
                else:
                    self._master.destroy() 

            
            # ...

            # Task 1.2 Mouse Controls: Remove the block from the world & get its drops
            # ...
            self._world.remove_block(block)
            drops = block.get_drops(luck, was_item_suitable)  
            

            

            if not drops:
                return

            x0, y0 = block.get_position()

            for i, (drop_category, drop_types) in enumerate(drops):
                print(f'Dropped {drop_category}, {drop_types}')

                if drop_category == "item":
                    physical = DroppedItem(create_item(*drop_types))

                    # this is so bleh
                    x = x0 - BLOCK_SIZE // 2 + 5 + (i % 3) * 11 + random.randint(0, 2)
                    y = y0 - BLOCK_SIZE // 2 + 5 + ((i // 3) % 3) * 11 + random.randint(0, 2)

                    self._world.add_item(physical, x, y)
                elif drop_category == "block":
                    self._world.add_block(create_block(*drop_types), x, y)
                else:
                    raise KeyError(f"Unknown drop category {drop_category}")

    def get_holding(self):
        active_stack = self._hot_bar.get_selected_value()
        active_item = active_stack.get_item() if active_stack else self._hands 

        effective_item = active_item if active_item.can_attack() else self._hands 

        return active_item, effective_item

    def check_target(self):
        # select target block, if possible
        active_item, effective_item = self.get_holding()

        pixel_range = active_item.get_attack_range() * self._world.get_cell_expanse()

        self._target_in_range = positions_in_range(self._player.get_position(),
                                                 self._target_position,
                                                   pixel_range)

    def _mouse_move(self, event):
        self._target_position = event.x, event.y
        self.check_target()

        

    def _left_click(self, event):
        # Invariant: (event.x, event.y) == self._target_position
        #  => Due to mouse move setting target position to cursor
        x, y = self._target_position

        if self._target_in_range:
            block = self._world.get_block(x, y)
            if block:
                self.mine_block(block, x, y)

    def _trigger_crafting(self, craft_type):
        CRAFTING_RECIPES_2x2 = [(((None, 'wood'),(None, 'wood')),Stack(create_item("stick"), 4)),
        (((None, 'dirt'),(None, 'wood')),Stack(create_item("stone"), 4)),(((None, 'dirt'),(None, 'dirt')),Stack(create_item("wood"), 4)),
        ((("wood", 'dirt'),("wood", 'dirt')),Stack(create_item("apple"), 4))]

        print(f"Crafting with {craft_type}")
        crafter = GridCrafter(CRAFTING_RECIPES_2x2)
       
        show_crafter = CraftingWindow(self._master, "crafting", self._hot_bar, self._inventory, crafter)



    def run_effect(self, effect):
        if len(effect) == 2:
            if effect[0] == "crafting":
                craft_type = effect[1]

                if craft_type == "basic":
                    
                    print("Can't craft much on a 2x2 grid :/")

                elif craft_type == "crafting_table":
                    print("Let's get our kraft® on! King of the brands")

                self._trigger_crafting(craft_type)
                return
            elif effect[0] in ("food", "health"):
                stat, strength = effect
                print(f"Gaining {strength} {stat}!")
                
                                      
                

                
                getattr(self._player, f"change_{stat}")(strength)
                self._status_view.set_food_value(self._player.get_food())
                self._status_view.set_health_value(self._player.get_health())
                if self._player.get_food() == 20 and self._player.get_health() < 20:
                    self._player.change_health(strength)
                    self._status_view.set_food_value(self._player.get_food())
                    self._status_view.set_health_value(self._player.get_health())
                    
                  
                return

        raise KeyError(f"No effect defined for {effect}")

    def _right_click(self, event):
        print("Right click")
       
        x, y = self._target_position
        target = self._world.get_thing(x, y)

        if target:
            # use this thing
            print(f'using {target}')
            effect = target.use()
            print(f'used {target} and got {effect}')

            if effect:
                self.run_effect(effect)
                

        else:
            # place active item
            selected = self._hot_bar.get_selected()

            if not selected:
                return

            stack = self._hot_bar[selected]
            drops = stack.get_item().place()

            stack.subtract(1)
            if stack.get_quantity() == 0:
                # remove from hotbar
                self._hot_bar[selected] = None

            if not drops:
                return

            # handling multiple drops would be somewhat finicky, so prevent it
            if len(drops) > 1:
                raise NotImplementedError("Cannot handle dropping more than 1 thing ")
            



            drop_category, drop_types = drops[0]

            x, y = event.x, event.y

            if drop_category == "block":
                existing_block = self._world.get_block(x, y)

                if not existing_block:
                    self._world.add_block(create_block(drop_types[0]), x, y)
                else:
                    raise NotImplementedError(
                        "Automatically placing a block nearby if the target cell is full is not yet implemented")

            elif drop_category == "effect":
                
                self.run_effect(drop_types)
                

            else:
                raise KeyError(f"Unknown drop category {drop_category}")

    def _activate_item(self, index):
        print(f"Activating {index}")

        self._hot_bar.toggle_selection((0, index))

    def _handle_player_collide_item(self, player: Player, dropped_item: DroppedItem, data,
                                    arbiter: pymunk.Arbiter):
        """Callback to handle collision between the player and a (dropped) item. If the player has sufficient space in
        their to pick up the item, the item will be removed from the game world.

        Parameters:
            player (Player): The player that was involved in the collision
            dropped_item (DroppedItem): The (dropped) item that the player collided with
            data (dict): data that was added with this collision handler (see data parameter in
                         World.add_collision_handler)
            arbiter (pymunk.Arbiter): Data about a collision
                                      (see http://www.pymunk.org/en/latest/pymunk.html#pymunk.Arbiter)
                                      NOTE: you probably won't need this
        Return:
             bool: False (always ignore this type of collision)
                   (more generally, collision callbacks return True iff the collision should be considered valid; i.e.
                   returning False makes the world ignore the collision)
        """

        item = dropped_item.get_item()

        if self._hot_bar.add_item(item):
            print(f"Added 1 {item!r} to the hotbar")
        elif self._inventory.add_item(item):
            print(f"Added 1 {item!r} to the inventory")
        else:
            print(f"Found 1 {item!r}, but both hotbar & inventory are full")
            return True

        self._world.remove_item(dropped_item)
        return False



class MenuBar(tk.Menu) :
    """Generic menubar for any window."""

    def __init__(self, master, menus) :
        """
        Parameters:
            master (Tk): Window in which this menu is to be displayed.
            menus (list[tuple(str, dict{str, func})]) :
                         Details of all the menus for this window.
                         List contains the entire set of menus.
                         Tuple is menu name string and dictionary of menu items.
                         Dictionary is menu item name mapped to event handler.
        """
        name_of_menu = 0
        items_of_menu = 1
        super().__init__(master)
        master.config(menu=self)
        for menu_details in menus :
            menu_to_add = tk.Menu(self)
            self.add_cascade(label=menu_details[name_of_menu], menu=menu_to_add)
            for menu_item, event_handler in menu_details[items_of_menu].items() :
                menu_to_add.add_command(label=menu_item, command=event_handler)

class FoodItem(Item) :
    
    def __init__(self, id_, strength: float) :
        super().__init__(id_, max_stack=4)
        self._id = id_
        self._strength = strength
    
    def get_strength(self) :
        return self._strength
    def place(self) :
        return [("effect",("food", self._strength))]
    def get_id(self) :
        return self._id
    def attack(self, successful):
        pass
    def can_attack(self):
        pass

class ToolItem(Item) :
    def __init__(self, id_, tool_type: str, durability: float) :
        super().__init__(id_, max_stack=1)
        self._id = id_
        self._tool_type = tool_type
        self._durability = durability
    def set_durability(self,newDurability) :
        self._durability = newDurability
    def get_durability(self) :
        return self._durability
    def get_type(self) :
        return self._tool_type
    def can_attack(self):
        if self._durability > 0 :
            return True
        else :
            return False
    def attack(self, successful: bool):
        if successful :
            self._durability = self._durability
        else :
            self._durability -= 1
    def get_max_stack_size(self):
        return self._max_stack_size
    def get_max_durability(self):
        return self._durability

#class CraftingTableBlock(ResourceBlock) :
    #def __init__(self) :



# class Sheep(Mob):
#     def step(self, time_delta, game_data):
#         if self._steps % 20 == 0:
#             health_percentage = self._health / self._max_health
#             x,y = self.get_velocity()
#             velocity = x + 5, y + 0
#             self.set_velocity(velocity)
        
#         super().step(time_delta, game_data)

#     def use(self):
#         pass
        





def main() :
    root = tk.Tk()
    app = Ninedraft(root)
    root.mainloop()

if __name__ == '__main__' :
    main()



