from api import *

class Tetromino:

    def __init__(self, name, size, color, shape, position, debug=False):
        '''
            get a random current rotation at object creation with max rotation
            volume_shape : pixel number in one shape
        '''
        self.surface_size = size
        self.name = name
        self.color = color
        self.shape = self.prepare_shape_data_as_one_tuple(shape)
        self.max_rotations = len(shape)
        self.previous_rotation = 0
        self.current_rotation = 0
        self.current_top_left_position = position
        self.surface_position = position
        self.position = position
        self.bottom_check = 0
        self.right_check = 0
        self.volume_shape = 16
        self.update_surface = False

        if debug == True:
            self.debug_draw_all()

    def prepare_shape_data_as_one_tuple(self, data):
        '''
            prepare a single tupple with the shape data and return it
        '''
        shapelist = []
        for shape in data:
            for line in range(4):
                for pixel in range(4):
                    try:
                        if shape[line][pixel] == 1:
                            shapelist.append(1)
                        else:
                            shapelist.append(0)
                    except IndexError:
                        shapelist.append(0)

        shapetuple = tuple(shapelist)
        return shapetuple

    def debug_draw_all(self):
        '''
            draw all shapes in text from the tuple
        '''
        print(self.name)
        print(self.color)
        for rotation in range(self.max_rotations):
            self.start = rotation*self.volume_shape
            for pixel in range(self.volume_shape):
                print(self.shape[self.start+pixel], end='')
                if pixel%4 == 3:
                    print('')
            print('****')

    def debug_draw(self):
        print(self.name)
        print(self.color)
        print('position : ' + str(self.current_rotation))
        self.start = self.current_rotation*self.volume_shape
        for pixel in range(self.volume_shape):
            print(self.shape[self.start+pixel], end='')
            if pixel%4 == 3:
                print('')

    def draw(self, surface, grid, debug=False):
        '''
            draw the shape on the given surface with the current rotation
            loop the self.shape built tupple using a cursor with self.start
        '''
        self.start = self.current_rotation*self.volume_shape
        x, y = self.position[0], self.position[1]
        for pixel in range(self.volume_shape):
            if self.shape[self.start+pixel] == 1:
                rectangle(surface,(x*grid,y*grid,grid,grid),self.color)
            x += 1
            if pixel%4 == 3:
                y += 1
                x = self.position[0]
        self.update_surface = False

        if debug == True:
            self.debug_draw()

    def move(self, direction):
        '''
          | check if next position is possible
          | if yes :
          | * save previous position
          | * uptade position
          | * play movement sound
          | * else play the blocked sound
        '''
        print(direction)
        self.update_surface = True

    def rotate(self, rotation):
        '''
          | check if next rotation is possible
          | if yes :
          | * save previous rotation
          | * get the next rotation
          | * play rotating sound
          | * else play the blocked sound
        '''
        self.previous_rotation = self.current_rotation
        self.current_rotation = (self.current_rotation + 1)%self.max_rotations
        self.update_surface = True

    def check_next_position(self, next_position):
        '''
            return True if the Tetromino can move
        '''
        pass

class Board:
    def __init__(self, data):
        self.surface_size = data['surface_size']
        self.surface_position = data['surface_position']
        self.width = data['surface_size'][0]
        self.height = data['surface_size'][1]
        self.update_surface = False

    def draw(self, surface, grid, color='grey', debug=False):
        '''
            Draw the Board borders
            Draw the Board content
            Draw the Grid if debug is on
        '''
        self.draw_borders(surface, grid, color='grey')
        self.update_surface = False

        if debug == True:
            self.draw_grid(surface,grid,'red')

    def draw_borders(self, surface, grid, color):
        rectangle(surface, (0,0,grid,self.height),color)
        rectangle(surface, (grid,self.height-grid,self.width-grid,grid),color)
        rectangle(surface, (self.width-grid,0,grid,self.height-grid),color)

    def draw_grid(self, surface, grid, color):
        for x in range(0, self.width, grid):
            for y in range(0, self.height, grid):
                line(surface,(0,y), (self.width, y), color)
                line(surface,(x,0), (x, self.height), color)

class Stats:
    def __init__(self, data):
        self.update_surface = False
        self.surface_size = data['surface_size']
        self.surface_position = data['surface_position']
        self.next_box = (data['position_next'],data['size_next'])
        self.stats = data['stats']

    def draw(self, surface, grid, font, debug=False):
        '''
            Draw the next tetromino box
            Draw the stats titles
            Draw the stats data
            Draw the grid if debug is on
        '''
        self.draw_next_box(surface, grid, self.next_box)
        self.draw_stats(font, surface, grid, self.stats)
        self.update_surface = False

    def draw_next_box(self, surface, grid, box):
        x = box[0][0]
        y = box[0][1]
        width = box[1][0]
        height = box[1][1]
        rectangle(surface,(x,y,grid,height))
        rectangle(surface,(x,height-grid,width,grid))
        rectangle(surface,(x+width-grid,y,grid,height))

    def draw_stats(self, font, surface, grid, stats):
        for stat in stats:
            title = stat[0]
            x = stat[1][0]
            y = stat[1][1]
            write(font, surface, (x,y), title)
            variable = stat[2]
            if variable is not None:
                write(font, surface, (x,y+grid), variable, 'white')

class Arrow:
    def __init__(self, data):
        '''
          | update surface flag
        '''
        self.update_surface = False
        self.surface_size = data['surface_size']
        self.selection = 0
        self.target = 0
        self.shape = None
        self.color = None
        self.transparent_color = 'pink'
        self.previous_position = (0,0)
        self.position = (0,0)
        self.index_max = 0

    def draw(self, surface):
        x = 0
        y = 0
        for i in self.shape:
            for j in i:
                if j == 1:
                    pixel(surface, (x,y), self.color)
                else:
                    pixel(surface, (x,y), self.transparent_color)
                x += 1
            y += 1
            x = 0
        self.update_surface = False

    def update_selection(self, direction):
        self.selection += direction
        if self.selection < 0:
            self.selection = self.index_max
        elif self.selection > self.index_max:
            self.selection = 0
        self.previous_position = self.position

    def move(self, key, state):
        '''
          | change position of the key
          | At game state Menu (3), arrows used to select an other game state
          | At game state New Game (4), arrows used to change settings  (name, speed)
          | keys :
          | 0 : UP
          | 1 : DOWN
          | 2 : LEFT
          | 3 : RIGHT
        '''
        if state == 3:
            if key == 0:
                self.update_selection(-1)
            elif key == 1:
                self.update_selection(1)
        elif state == 5:
            if key == 0:
                #change setting function
                print("change setting")
            elif key == 1:
                #change setting function
                print("change setting")
            elif key == 2:
                self.update_selection(-1)
            elif key == 3:
                self.update_selection(1)

    def get_data(self, content):
        '''
          | get the arrow data from current selection
          | position, color and target
        '''
        self.index_max = len(content['arrowselect']) - 1
        self.shape = content['arrowshape']
        options = content['arrowselect'][self.selection]
        self.position = options[0]
        self.color = options[1]
        self.target = options[2]
