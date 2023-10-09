import pyglet
import pyglet.gl as pygletGL
from pyglet.window import key
import random
import time
import os
pyglet.resource.path = ['../Asset', '../Asset/fonts', '../Asset/sprites']
pyglet.resource.reindex()
pyglet.font.add_file(pyglet.resource.file('NotJamToolkit15.ttf')) #FONT NAME: NotJamToolkit15
pyglet.font.add_file(pyglet.resource.file('Not Jam Third Dimension 19.ttf')) #FONT NAME: Not Jam Third Dimension 19
pyglet.font.add_file(pyglet.resource.file('NotJamBlackletter13.ttf')) #FONT NAME: NotJamBlkltr13
pyglet.font.add_file(pyglet.resource.file('NotJamChunkySans.ttf')) #FONT NAME: NotJamChunkySans
pyglet.font.add_file(pyglet.resource.file('NotJamScrawl12.ttf')) #FONT NAME: NotJamScrawl12
pyglet.font.add_file(pyglet.resource.file('Not Jam Signature 21.ttf')) #FONT NAME: Not Jam Signature 21
pyglet.font.add_file(pyglet.resource.file('NotJamSlabSerif11.ttf')) #FONT NAME: NotJamSlabSerif1
"""GLOBAL VARIABLE"""
game_screen = pyglet.window.Window(1500,800)
keys = key.KeyStateHandler()
tempclock = pyglet.clock.get_default()
anotherClock  = pyglet.clock.get_default()

load_title_screen_resources = pyglet.graphics.Batch()
load_battle_scene_labels = pyglet.graphics.Batch()

background_screen = None
background_screen2 = None
button_Adventure = None
button_Upgrade = None
button_Return = None
game_titleLBL = None
game_startbuttonLBL = None
game_exitbuttonLBL = None
game_AdventureLBL = None
game_UpgradeLBL = None
game_ReturnLBL = None

game_BattleAnnounceLBL = None
game_BattleAttackLBL = None
game_BattleRunLBL = None
game_BattleTurnLBL = None
game_BattleDamageDealtLBL = None
game_BattleMonsterHealthLBL = None
game_BattlePlayerHealthLBL = None

sprite_player = None
sprite_monster = None
sprite_width = 0
sprite_radius = 0

battle_turn = True
animate_out = False
player_name = None
player_health = 100
player_current_health = 20
player_lowest_Attack = 1
player_highest_Attack = 10
player_level = 1

monster_name = 'Goblin'
monster_health = 100
monster_current_health = monster_health
monster_lowest_Attack = 1
monster_highest_Attack = 10
monster_level = 1

is_on_titlescreen = True
is_on_battlescene = False
is_on_maingame = False

"""FUNCTIONS"""
def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

def Animate_Sprite(image,rowsSprite, columnsSprite, duration=0.1, scale_sprite = 5, scaleX_sprite = 1):
    global sprite_width
    global sprite_radius
    sprite_sheet = pyglet.resource.image(image)
    image_grid = pyglet.image.ImageGrid(sprite_sheet, rows=rowsSprite, columns=columnsSprite,)
    ani = pyglet.image.Animation.from_image_sequence(image_grid, duration=duration)
    sprite_width = ani.get_max_width()
    sprite_radius = sprite_width // 2
    ani_sprite = pyglet.sprite.Sprite(ani)
    ani_sprite.update(scale= scale_sprite, scale_x= scaleX_sprite)
    return ani_sprite

def Load_Title_Screen():
    global game_titleLBL
    global game_startbuttonLBL
    global game_exitbuttonLBL
    global background_screen
    global background_screen2
    global is_on_titlescreen
    background_screen2 = pyglet.sprite.Sprite(pyglet.resource.image('TitleScreenbackgroundLayer2.png'), 
                                             batch=load_title_screen_resources)
    background_screen = pyglet.sprite.Sprite(pyglet.resource.image('TitleScreenbackground.png'), 
                                             batch=load_title_screen_resources)
    background_screen.opacity = 80
    background_screen.update(scale=10)
    background_screen2.opacity = 80
    background_screen2.update(scale=10)
    game_titleLBL = pyglet.text.Label('Endless Adventure', 
                                font_name='Not Jam Signature 21',
                                color=(160, 27, 20, 255), 
                                font_size=150 , x=game_screen.width - 1350, 
                                y=game_screen.height - 200,
                                batch=load_title_screen_resources)
    game_startbuttonLBL = pyglet.text.Label('START', 
                                        font_name='NotJamToolkit15', 
                                        font_size=60, 
                                        color=(255, 206, 128, 255), 
                                        x=game_screen.width - 950, 
                                        y=game_screen.height - 450,
                                        batch=load_title_screen_resources)
    game_exitbuttonLBL = pyglet.text.Label(' EXIT', 
                                        font_name='NotJamToolkit15', 
                                        color=(255, 206, 128, 255), 
                                        font_size=60, x=game_screen.width - 950, 
                                        y=game_screen.height - 600,
                                        batch=load_title_screen_resources)
    is_on_titlescreen = True
    
    
def Load_Entity():
    global sprite_player
    global sprite_monster  
    sprite_player = Animate_Sprite('Player/Idle.png', 1, 11)
    sprite_monster = Animate_Sprite('Goblin/Idle.png', 1, 4)
    sprite_player.x = sprite_monster.x = game_screen.width
    
def Leaving_Title_Screen(dt):
    if sprite_player.x !=100:
        sprite_player.x -= 1000 * dt
    
def Animate_Out_Title_Screen(dt):
    if game_startbuttonLBL.y != 500:
        game_startbuttonLBL.y -= 1000 * dt
    if game_exitbuttonLBL.y != 500:
        game_exitbuttonLBL.y -= 1000 * dt
    if game_titleLBL.y != 500:
        game_titleLBL.y += 1000 * dt
    if background_screen.opacity != 100:
        background_screen.opacity += 200 * dt

def Remove_Title_Screen():
    global tempclock
    global is_on_titlescreen
    pyglet.clock.Clock.schedule_interval_for_duration(tempclock,
                                                    func=Animate_Out_Title_Screen,
                                                    interval=1/60,
                                                    duration=0.8)
    global sprite_player
    sprite_player = Animate_Sprite('Player/Run.png', 1, 8, scale_sprite=15, scaleX_sprite=-1)
    sprite_player.x = (game_screen.width - sprite_radius) + 1300
    sprite_player.y = -1000
    pyglet.clock.Clock.schedule_interval_for_duration(tempclock,
                                                    func=Leaving_Title_Screen,
                                                    interval=1/60,
                                                    duration=2)

def Load_Main_Game(dt):
    global background_screen
    global sprite_player
    global button_Adventure
    global button_Upgrade
    global button_Return
    global is_on_maingame
    global tempclock
    global is_on_titlescreen
    global game_AdventureLBL
    global game_UpgradeLBL
    global game_ReturnLBL
    background_screen = pyglet.sprite.Sprite(pyglet.resource.image('MainGamebackground.png'))
    background_screen.scale= 2.5
    background_screen.scale_x= 1.09
    
    sprite_player = Animate_Sprite('Player/Idle.png', 1, 11, scale_sprite=19, scaleX_sprite=-1)
    sprite_player.x = (game_screen.width - sprite_radius) + 1100
    sprite_player.y = -1200
    
    button_Adventure = pyglet.sprite.Sprite(pyglet.resource.image('UI/Button.png'))
    button_Adventure.scale = 15
    button_Adventure.y = game_screen.height
    game_AdventureLBL = pyglet.text.Label('Adventure', 
                                          font_name='NotJamBlkltr13', 
                                          x=game_screen.width - 1440, y=game_screen.height - 200, 
                                          font_size=70, color=(207, 137, 76, 255))
    
    button_Upgrade = pyglet.sprite.Sprite(pyglet.resource.image('UI/Button.png'))
    button_Upgrade.scale = 15
    button_Upgrade.y = game_screen.height
    game_UpgradeLBL = pyglet.text.Label('Upgrade', 
                                        font_name='NotJamBlkltr13', 
                                        x=game_screen.width - 1440, y=game_screen.height - 450, 
                                        font_size=90, color=(245, 92, 69, 255))
    
    button_Return = pyglet.sprite.Sprite(pyglet.resource.image('UI/Button.png'))
    button_Return.scale = 15
    button_Return.y = game_screen.height
    game_ReturnLBL = pyglet.text.Label('Return', 
                                       font_name='NotJamBlkltr13', 
                                       x=game_screen.width - 1405, y=game_screen.height - 700, 
                                       font_size=90)
    
    pyglet.clock.Clock.schedule_interval_for_duration(tempclock, Animate_Button_On_MainGame, 1/60, 0.9)
    is_on_maingame = True
    is_on_titlescreen = False
    
def Animate_Button_On_MainGame(dt):
    if button_Adventure.y != (game_screen.height - 300):
        button_Adventure.y -= 25
        
    if button_Upgrade.y != (game_screen.height - 550):
        button_Upgrade.y -= 25
        
    if button_Return.y != (game_screen.height - 800):
        button_Return.y -= 25
        
def Animate_Out_MainGame(dt):
    if button_Adventure.y >= (game_screen.height - 300):
        button_Adventure.y += 30
        game_AdventureLBL.y += 30
        
    if button_Upgrade.y >= (game_screen.height - 550):
        button_Upgrade.y += 30
        game_UpgradeLBL.y += 30
        
    if button_Return.y >= (game_screen.height - 800):
        button_Return.y += 30
        game_ReturnLBL.y += 30
        
    if sprite_player.x !=100:
        sprite_player.x -= 1600 * dt
        
    if background_screen.opacity != 0:
        background_screen.opacity -= 5
        
def Leaving_MainGame():
    global tempclock
    global sprite_player
    global is_on_maingame
    pyglet.clock.Clock.schedule_interval_for_duration(tempclock,
                                                    func=Animate_Out_MainGame,
                                                    interval=1/60,
                                                    duration=1.3)
    sprite_player = Animate_Sprite('Player/Run.png', 1, 8, scale_sprite=19, scaleX_sprite=-1)
    sprite_player.x = (game_screen.width - sprite_radius) + 1100
    sprite_player.y = -1200
    
def Animate_Battle_Intro(dt):
    global game_BattleAnnounceLBL
    if game_BattleAnnounceLBL.opacity > 0:
        game_BattleAnnounceLBL.opacity -= 5
    if background_screen.opacity < 200:
        background_screen.opacity += 5
    if sprite_player.opacity < 255:
        sprite_player.opacity += 5
    if sprite_monster.opacity < 255:
        sprite_monster.opacity += 5

def Generate_Player():
    global sprite_player
    sprite_player = Animate_Sprite('Player/Idle.png', 1, 11, scaleX_sprite=-1, scale_sprite=8)
    sprite_player.opacity = 0
    sprite_player.x = 1800
    sprite_player.y = -320

def Generate_Monster():
    global sprite_monster
    sprite_monster = Animate_Sprite('Goblin/Idle.png', 1, 4, scale_sprite=7)
    sprite_monster.opacity = 0
    sprite_monster.x = -300
    sprite_monster.y = -210

def Load_Battle_Scene(dt):
    is_on_maingame = False
    global game_BattleAnnounceLBL
    global is_on_battlescene
    global background_screen
    
    global game_BattleAttackLBL
    global game_BattleRunLBL
    game_BattleAnnounceLBL = pyglet.text.Label('ENEMY ENCOUNTER', 
                                font_name='Not Jam Signature 21',
                                color=(160, 27, 20, 255),
                                font_size=110, anchor_x='center',
                                x=game_screen.width // 2, y=game_screen.height // 2,
                                batch=load_battle_scene_labels)

    game_BattleAttackLBL = pyglet.text.Label('attack', 
                                font_name='Not Jam Signature 21',
                                font_size=50, anchor_x='center',
                                x=1119, y=385)
    game_BattleAttackLBL.opacity = 0
    game_BattleRunLBL = pyglet.text.Label('run', 
                                font_name='Not Jam Signature 21',
                                font_size=50, anchor_x='center',
                                x=1080, y=333)
    game_BattleRunLBL.opacity = 0
    Generate_Player()
    Generate_Monster()
    background_screen = pyglet.sprite.Sprite(pyglet.resource.image('Battlebackground.png'))
    background_screen.opacity = 0
    background_screen.scale = 2
    pyglet.clock.Clock.schedule_interval_for_duration(tempclock, Animate_Battle_Intro, 1/60, 1.8)
    is_on_battlescene = True
    pyglet.clock.schedule_interval(On_Battle, 1)
    
def On_Battle(dt):
    global battle_turn
    global game_BattlePlayerHealthLBL, game_BattleMonsterHealthLBL
    global player_current_health, player_health
    global monster_current_health, monster_health
    global sprite_player, sprite_monster
    game_BattlePlayerHealthLBL = pyglet.text.Label(str(player_current_health) + ' / ' + str(player_health), 
                                font_name='Not Jam Signature 21',
                                font_size=50, anchor_x='center',
                                x=1235, y=555,
                                batch=load_battle_scene_labels)
    game_BattleMonsterHealthLBL = pyglet.text.Label(str(monster_current_health) + ' / ' + str(monster_health), 
                                font_name='Not Jam Signature 21',
                                font_size=50, anchor_x='center',
                                x=250, y=555,
                                batch=load_battle_scene_labels)
    if player_current_health <= 0:
        pyglet.clock.Clock.schedule_interval_for_duration(tempclock, Animate_Player_Death, 1/60, 0.5)
        pyglet.clock.schedule_once(Animate_Plater_LastFrameDeath, 1.3) 
        pyglet.clock.unschedule(On_Battle)              
    if battle_turn == True:
        global counter
        counter = 0
        Animate_Player_Turn()
    elif battle_turn == False:
        pyglet.clock.schedule_once(Animate_Monster_Turn, 0.5)
        pyglet.clock.schedule_once(Monster_Attack, 0.5)
        game_BattleAttackLBL.opacity = 0
        game_BattleRunLBL.opacity = 0

def Animate_Player_Death(dt):
    global sprite_player
    sprite_player = Animate_Sprite('Player/Death.png', 1, 9, scaleX_sprite=-1, scale_sprite=8)
    sprite_player.x = 1800
    sprite_player.y = -320
    
def Animate_Plater_LastFrameDeath(dt):
    global sprite_player
    global is_on_battlescene
    global game_BattleAnnounceLBL
    global background_screen
    sprite_player = Animate_Sprite('Player/Death11.png', 1, 1, scaleX_sprite=-1, scale_sprite=8)
    sprite_player.x = 1700
    sprite_player.y = -320
    game_BattleAnnounceLBL = pyglet.text.Label('YOU DIED', 
                                font_name='Not Jam Signature 21',
                                color=(250, 27, 20, 255),
                                font_size=110, anchor_x='center',
                                x=game_screen.width // 2, y=game_screen.height // 2,
                                batch=load_battle_scene_labels)
    game_BattleAnnounceLBL.opacity = 255
    background_screen.opacity = 100
    # is_on_battlescene = False
    

def Animate_Player_Turn():
    global game_BattleTurnLBL
    global animate_out
    game_BattleTurnLBL = pyglet.text.Label('YOUR TURN', 
                        font_name='NotJamScrawl12',
                        font_size=100, anchor_x='center',
                        x=game_screen.width // 2, y=650,
                        batch=load_battle_scene_labels)
    game_BattleAttackLBL.opacity = 255
    game_BattleRunLBL.opacity = 255

def Animate_Monster_Turn(dt):
    global game_BattleTurnLBL
    game_BattleTurnLBL = pyglet.text.Label('ENEMY TURN', 
                        font_name='NotJamScrawl12',
                        font_size=100, anchor_x='center',
                        x=game_screen.width // 2, y=650,
                        batch=load_battle_scene_labels)
  
def Animate_Player_Attack(dt):
    global sprite_player
    global animate_out
    game_BattleAttackLBL.opacity = 0
    game_BattleRunLBL.opacity = 0
    if battle_turn:
        if sprite_player.x > 1000:
            sprite_player.x -= 50
        elif sprite_player.x == 1000:
            sprite_player = Animate_Sprite('Player/Attack.png', 1, 6, scaleX_sprite=-1, scale_sprite=8, duration=0.07)
            sprite_player.x = 1001
            sprite_player.y = -320

def Change_var_animate_out(dt):
    global animate_out
    animate_out = True
            
def AnimateOut_Player_Attack(dt):
    global sprite_player
    global animate_out
    game_BattleAttackLBL.opacity = 0
    game_BattleRunLBL.opacity = 0
    if animate_out == True:
        if sprite_player.x == 1001: 
            sprite_player = Animate_Sprite('Player/Idle.png', 1, 11, scaleX_sprite=-1, scale_sprite=8)
            sprite_player.x = 1000
                
        if sprite_player.x != 1800:
            sprite_player.x += 50
            sprite_player.y = -320
        else:
            animate_out = False
            
def Monster_Attack(dt):
    Monster_deal_damage()
    pyglet.clock.Clock.schedule_interval_for_duration(tempclock, Animate_Monster_Attack, 1/60, 1)
    pyglet.clock.schedule_once(Change_var_animate_out, 1)
    pyglet.clock.Clock.schedule_interval_for_duration(tempclock, AnimateOut_Monster_Attack, 1/60, 2)
    pyglet.clock.schedule_once(Change_Battle_Turn_To_Player, 1)
    
    
counter = 0  
def Monster_deal_damage():
    global counter
    global player_current_health
    if counter == 0:
        damage_dealt_to_player = Calculate_Damage_Dealt(monster_lowest_Attack, monster_highest_Attack)
        player_current_health -= damage_dealt_to_player
        counter += 1

def Animate_Monster_Attack(dt):
    global sprite_monster
    if battle_turn == False:
        if sprite_monster.x < 550:
            sprite_monster.x += 50
        elif sprite_monster.x == 550:
            sprite_monster = Animate_Sprite('Goblin/Attack.png', 1, 8, scale_sprite=7, duration=0.07)
            sprite_monster.x = 551
            sprite_monster.y = -210

def AnimateOut_Monster_Attack(dt):
    global sprite_monster
    global animate_out
    if animate_out == True:
        if sprite_monster.x == 551:
            sprite_monster = Animate_Sprite('Goblin/Idle.png', 1, 4, scale_sprite=7)
            sprite_monster.x = 550
            sprite_monster.y = -210
        
        if sprite_monster.x != -300:
            sprite_monster.x -= 50
            sprite_monster.y = -210
        else:
            animate_out = False

def Change_Battle_Turn_To_Enemy(dt):
    global battle_turn
    if battle_turn == True:
        battle_turn = False
        
def Change_Battle_Turn_To_Player(dt):
    global battle_turn
    if battle_turn == False:
        battle_turn = True
    
def Calculate_Damage_Dealt(lowAtk, highAtk):
    rndDamage = random.uniform(lowAtk, highAtk)
    calculated_damage = round(rndDamage)
    return calculated_damage

def Animate_Damage_Dealt(dt):
    global battle_turn
    if sprite_player.x <= 1001:
            if game_BattleDamageDealtLBL.opacity != 255:
                game_BattleDamageDealtLBL.opacity += 15
                if game_BattleDamageDealtLBL.y != 450 and game_BattleDamageDealtLBL.opacity > 230:
                    game_BattleDamageDealtLBL.y += 50
                    
    if sprite_player.x >= 1800:
            game_BattleDamageDealtLBL.opacity = 0

"""GAME LOAD RESOURCES"""
Load_Title_Screen()
Load_Entity()
# pyglet.clock.schedule_once(Load_Battle_Scene, 0)
@game_screen.event
def on_draw():
    """makes pixel smooth"""
    pygletGL.glTexParameteri(pygletGL.GL_TEXTURE_2D, pygletGL.GL_TEXTURE_MAG_FILTER, pygletGL.GL_NEAREST) 
    pygletGL.glTexParameteri(pygletGL.GL_TEXTURE_2D, pygletGL.GL_TEXTURE_MIN_FILTER, pygletGL.GL_NEAREST)
    
    game_screen.clear()
    if is_on_titlescreen:
        load_title_screen_resources.draw()
    
    background_screen.draw()
    sprite_player.draw()

    if is_on_maingame:
        button_Adventure.draw()
        button_Upgrade.draw()
        button_Return.draw()
        game_AdventureLBL.draw()
        game_UpgradeLBL.draw()
        game_ReturnLBL.draw()
        
    if is_on_battlescene:
        sprite_monster.draw()
        load_battle_scene_labels.draw()
        game_BattleAttackLBL.draw()
        game_BattleRunLBL.draw()
        
@game_screen.event
def on_mouse_press(x, y, button, modifiers):
    """START BUTTON"""
    print(x,y)
    if is_on_titlescreen:
        """START BUTTON CLICKED"""
        if x > 540 and y > 340:
            if x < 890 and y < 420:
                Remove_Title_Screen()
                pyglet.clock.schedule_once(Load_Main_Game, 2)
                
    if is_on_maingame:
        """ADVENTURE BUTTON CLICKED"""
        if x > 20 and y > 520:
            if x < 700 and y < 720:
                Leaving_MainGame()
                pyglet.clock.schedule_once(Load_Battle_Scene, 1.5)
                
        """UPGRADE BUTTON CLICKED"""
        if x > 20 and y > 270:
            if x < 700 and y < 460:
                pass
        """RETURN BUTTON CLICKED"""
        if x > 20 and y > 20:
            if x < 700 and y < 220:
               pass
    
    if battle_turn:
        """ATTACK BUTTON CLICKED"""
        if x > 1057 and y > 384:
            if x < 1178 and y < 415:
                global game_BattleDamageDealtLBL
                global monster_current_health
                damage_dealt = Calculate_Damage_Dealt(player_lowest_Attack, player_highest_Attack)
                monster_current_health -= damage_dealt
                game_BattleDamageDealtLBL = pyglet.text.Label(str(damage_dealt), 
                                font_name='Not Jam Signature 21',
                                font_size=50, anchor_x='center',
                                x=250, y=300,
                                batch=load_battle_scene_labels)
                game_BattleDamageDealtLBL.opacity = 0
                pyglet.clock.Clock.schedule_interval_for_duration(tempclock, Animate_Player_Attack, 1/60, 1)
                pyglet.clock.schedule_once(Change_var_animate_out, 1)
                pyglet.clock.Clock.schedule_interval_for_duration(tempclock, AnimateOut_Player_Attack, 1/60, 2)
                pyglet.clock.Clock.schedule_interval_for_duration(tempclock, Animate_Damage_Dealt, 1/60, 2)
                pyglet.clock.schedule_once(Change_Battle_Turn_To_Enemy, 1)

    """EXIT BUTTON"""

# @game_screen.event
# def on_key_press(symbol, modifiers):
    
if __name__ == '__main__':
    # event_logger = pyglet.window.event.WindowEventLogger()
    # game_screen.push_handlers(event_logger)
    pyglet.app.run()
    
    
