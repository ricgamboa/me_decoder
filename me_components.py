# Module with the classes used for the sender definition

import secrets


class Sender:
    # Sender is the user that will send encrypted characters

    def __init__(self, id_number, name):
        self.id = id_number
        self.name = name
        self.icons = []
        self.cell = 0

    def find_icon(self, position_list):
        # find the icon with a given position list
        position = position_list[self.cell]
        icon = self.icons[position]
        return icon


class Icons:
    # Icons is a list of icons used by the sender to choose the alphabet
    def __init__(self, collection_size):
        self.collection = list(range(collection_size))

    def random_choose(self, num):
        # Choose random icons from the collection
        chosen = []
        rest = self.collection.copy()
        for i in range(num):
            pos = secrets.randbelow(len(rest))
            chosen.append(rest[pos])
            rest.pop(pos)
        return chosen

    def random_order(self):
        # Change the set to random order
        random_set = self.random_choose(len(self.collection))
        return random_set

    def group_icons(self, num_groups):
        # group the icons set
        group_size = len(self.collection)/num_groups
        group = []
        last_index = 0
        for count in range(num_groups-1):
            next_index = int((count + 1) * group_size)
            group.append(self.collection[last_index:next_index])
            last_index = next_index
        group.append(self.collection[last_index:])
        return group

    def find_group(self, icon, num_groups):
        # find the group for a specific icon
        group_index = 0
        for group in self.group_icons(num_groups):
            if icon in group:
                break
            group_index += 1
        return group_index


class PositionList:
    # PositionList is a list with possible positions of the icons, the user must choose a cell with the position
    def __init__(self, list_size, num_positions):
        trivial = True

        while trivial:
            self.list = []
            for i in range(list_size):
                self.list.append(secrets.randbelow(num_positions))
            trivial = self.is_trivial(range(num_positions))

    def is_trivial(self, elements):
        # Check if the list is trivial because does not have all the elements required
        found_list = []
        for i in elements:
            if elements[i] in self.list:
                found_list.append(True)
            else:
                found_list.append(False)

        if False in found_list:
            return True
        else:
            return False

    def random_cell(self):
        return secrets.randbelow(len(self.list))


class Question:
    # Question includes the information to show to the customer

    def __init__(self, id_number, num_answer_letters):
        self.id = id_number
        self.num_answer_letters = num_answer_letters
        self.icons_set = []
        self.pos_list_set = []

    def append_icon_set(self, new_set):
        # Add icon set to the question
        icon_set = Icons(len(new_set))
        icon_set.collection = new_set
        self.icons_set.append(icon_set)

    def append_position_list(self, new_pos):
        # Add position list to the question
        position_list = PositionList(len(new_pos), 1)
        position_list.list = new_pos
        self.pos_list_set.append(position_list)
