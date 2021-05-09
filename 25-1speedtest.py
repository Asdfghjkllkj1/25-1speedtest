import random as r
import time
from datetime import datetime
import pygame
import colorama
from colorama import *
import sys

try:
    arg = sys.argv[1]
    if arg == '--comp' or arg == '-c':
        raise IndexError
except IndexError:
    arg = None
colorama.init(autoreset=True)
if arg == '-h' or arg == '-?' or arg == '--help':
    print(f'25-1 SpeedTest | Asdfghjkllkj, 5/9/2021; v1.0.0\n'
          f'Commands (syntax: 25-1speedtest.py [1 OPTION]): \n'
          f'\t-h / -? / --help  {Fore.LIGHTBLACK_EX}|{Style.RESET_ALL}  Prints this message, then exits\n'
          f'\t-c / --comp       {Fore.LIGHTBLACK_EX}|{Style.RESET_ALL}  Enters competition mode (default)\n'
          f'\t-ca / --casual    {Fore.LIGHTBLACK_EX}|{Style.RESET_ALL}  Enters casual mode\n'
          f'\nExample: \n'
          f'\tpython 25-1speedtest.py --casual')
    exit(0)
casual = [False, True][arg == '-ca' or arg == '--casual']
ROWS = 5
COLUMNS = 5
r.shuffle(board := list(range(1, 26)))
board = [board[i:i + ROWS] for i in range(0, len(board), COLUMNS)]
player_enter = []
pygame.init()
screen = pygame.display.set_mode(size := (WIDTH := len(board) * 100, HEIGHT := len(board[0]) * 100))
pygame.display.set_caption('25 - 1 Speed Test')
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load('icon.png'))
font = pygame.font.SysFont('Calibri', FONT_SIZE := 36)
FPS = 60
clicking, started, start_time = True, False, None
while clicking:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            clicking = False
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if len(player_enter) > 0 and event.key == pygame.K_LEFT:
                player_enter.pop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            started = True
            if started and start_time is None:
                start_time = time.time()
            mouse_pos = pygame.mouse.get_pos()
            if (selection := board[mouse_pos[1] // 100][mouse_pos[0] // 100]) not in player_enter:
                player_enter.append(selection)
            if len(player_enter) >= 25:
                clicking = False
                break
    screen.fill((255, 255, 255))
    [screen.blit(font.render(str(num), False, (0, 0, 0)),
                 (j * 100 + WIDTH // ROWS // 2 - FONT_SIZE // 2, i * 100 + HEIGHT // COLUMNS // 2 - FONT_SIZE // 2)) for
     i, row in enumerate(board) for j, num in enumerate(row) if num not in player_enter]
    pygame.display.flip()
    pygame.display.set_caption(f'25 - 1 Speed Test {time.time() - [time.time(), start_time][start_time is not None]}s')
    clock.tick(FPS)
pygame.quit()
if player_enter == list(range(25, 0, -1)):
    print(
        f'{Fore.BLUE}{Style.BRIGHT}you win!{Style.RESET_ALL}\ntime taken: {(time_taken := time.time() - start_time)}s')
    if float(time_taken) <= (prev_time := float((prev_score := open(
            filepath := ['highscores.txt', 'casuals.txt'][casual], 'r'
    ).readlines()[-1].rstrip()).split(';')[0])) or casual:
        open(filepath, 'a+').write(
            f'\n{str(time_taken).ljust(len(str(time_taken)) + (18 - len(str(time_taken))), "0")};'
            f'{str(datetime.now().strftime("%Y/%m/%d-%H:%M:%S"))} | '
            f'{input("username (no spaces; default=AnonymousUser): ") or "AnonymousUser"}')
        if arg is None:
            print(
                f'you beat previous score of {prev_time}s set by {prev_score.split(";")[1].split(" | ")[1]}'
                f' by {prev_time - time_taken}s')
        elif casual:
            print(f'You are playing casually. Change parameter to be "-c" to do competitions!')
    open('log.txt', 'a+').write(f'\n{str(time_taken).ljust(len(str(time_taken)) + (18-len(str(time_taken))), "0")};'
                                f'{str(datetime.now().strftime("%Y/%m/%d-%H:%M:%S"))}')
else:
    print(f'{Fore.RED}{Style.BRIGHT}u failed{Style.RESET_ALL} in {time.time() - start_time}s\n'
          f'your answer: \n\t{player_enter}')
