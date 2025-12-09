import pygame
import time
import math
import geometry
import sequences

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

WHITE = (255, 255, 255)
BG_COLOR = (20, 20, 20)       
GRID_LINE_COLOR = (50, 50, 50) 
CIRCLE_COLOR = (60, 60, 60)   
ACTIVE_COLOR = (0, 255, 200)  
SUCCESS_COLOR = (0, 255, 0)   
ERROR_COLOR = (255, 0, 0)     
TEXT_COLOR = (200, 200, 200)
ORANGE = (255, 165, 0)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER = (80, 80, 80)

GRID_SPACING = 120    
CIRCLE_SIZE = 25      

FLASH_FAST = 250      
FLASH_SLOW = 500  
PAUSE_DURATION = 50   

TRIALS_PER_RULE = 5

def save_trial_data(data):
    pass

def run_experiment():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("LoT 5x5 Experience")
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 28)

    save_trial_data(["Header"])

    positions = geometry.get_grid_coordinates(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, GRID_SPACING)

    full_queue = sequences.TRAINING_RULES + sequences.TEST_RULES
    stats = {rule: [0, 0, 0] for rule in sequences.TEST_RULES} 

    trial_idx = 0
    global_state = "INTRO" 
    replay_mode = False 
    
    current_rule_name = full_queue[0]
    current_sequence = []
    
    def start_trial(rule_name):
        nonlocal current_sequence, trial_state, current_step, is_lit, user_feedback, guess_start_time, current_flash_duration
        current_sequence = sequences.generate_sequence(rule_name)
        trial_state = "WATCH"
        current_step = 0
        is_lit = True
        user_feedback = ""
        guess_start_time = 0
        
        if rule_name in ["Sauts Incrémentaux", "Irrégulier"]:
            current_flash_duration = FLASH_SLOW
        else:
            current_flash_duration = FLASH_FAST

    current_flash_duration = FLASH_FAST
    start_trial(current_rule_name)

    trial_state = "WATCH"
    last_update_time = pygame.time.get_ticks()
    target_index = -1
    feedback_col = TEXT_COLOR
    
    ui_buttons = [] 

    running = True
    while running:
        screen.fill(BG_COLOR)
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if global_state == "FINISHED":
                    for btn in ui_buttons:
                        rect, action, payload = btn
                        if rect.collidepoint(mouse_pos):
                            if action == "REPLAY_RULE":
                                current_rule_name = payload
                                replay_mode = True
                                start_trial(current_rule_name)
                                global_state = "EXPERIMENT"
                            elif action == "RESTART_ALL":
                                trial_idx = 0
                                stats = {rule: [0, 0, 0] for rule in sequences.TEST_RULES}
                                current_rule_name = full_queue[0]
                                replay_mode = False
                                start_trial(current_rule_name)
                                global_state = "INTRO"
                            elif action == "QUIT":
                                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if global_state == "INTRO":
                        global_state = "EXPERIMENT"
                        last_update_time = current_time
                    elif global_state == "TRANSITION":
                        global_state = "EXPERIMENT"
                        last_update_time = current_time
            
            if event.type == pygame.MOUSEBUTTONDOWN and global_state == "EXPERIMENT" and trial_state == "GUESS":
                for i, pos in enumerate(positions):
                    dist = math.hypot(mouse_pos[0] - pos[0], mouse_pos[1] - pos[1])
                    
                    if dist < CIRCLE_SIZE + 15:
                        rt = current_time - guess_start_time
                        is_correct = (i == target_index)
                        
                        if is_correct:
                            user_feedback = "BRAVO !"
                            feedback_col = SUCCESS_COLOR
                        else:
                            user_feedback = "RATE !"
                            feedback_col = ERROR_COLOR

                        phase_name = "Training" if current_rule_name in sequences.TRAINING_RULES else "Test"
                        
                        if not replay_mode:
                            if phase_name == "Test":
                                stats[current_rule_name][0] += 1
                                if is_correct: stats[current_rule_name][1] += 1
                                stats[current_rule_name][2] += rt
                            save_trial_data(["No Data"])
                        
                        trial_state = "RESULT"
                        last_update_time = current_time

        if global_state == "EXPERIMENT":
            if trial_state == "WATCH":
                if current_step < len(current_sequence) - 1:
                    if is_lit:
                        if current_time - last_update_time > current_flash_duration:
                            is_lit = False
                            last_update_time = current_time
                    else:
                        if current_time - last_update_time > PAUSE_DURATION:
                            current_step += 1
                            is_lit = True
                            last_update_time = current_time
                else:
                    trial_state = "GUESS"
                    target_index = current_sequence[current_step]
                    guess_start_time = pygame.time.get_ticks()

            elif trial_state == "RESULT":
                if current_time - last_update_time > 1500:
                    if replay_mode:
                        global_state = "FINISHED" 
                        replay_mode = False
                    else:
                        trial_idx += 1
                        if trial_idx == len(sequences.TRAINING_RULES):
                            global_state = "TRANSITION"
                            current_rule_name = full_queue[trial_idx]
                            start_trial(current_rule_name)
                        elif trial_idx >= len(full_queue):
                            global_state = "FINISHED"
                        else:
                            current_rule_name = full_queue[trial_idx]
                            start_trial(current_rule_name)

        if global_state == "INTRO":
            draw_text_centered(screen, title_font, "EXPERIENCE DE SEQUENCES", -50, ACTIVE_COLOR)
            draw_text_centered(screen, font, "1. Memorisez la sequence de points bleus", 20, WHITE)
            draw_text_centered(screen, font, "2. A la fin, cliquez sur le point SUIVANT", 60, WHITE)
            draw_text_centered(screen, font, "Appuyez sur ESPACE pour commencer", 150, ORANGE)

        elif global_state == "TRANSITION":
            draw_text_centered(screen, title_font, "FIN DE L'ENTRAINEMENT", -50, SUCCESS_COLOR)
            draw_text_centered(screen, font, "Attention : Les sequences changent !", 20, WHITE)
            draw_text_centered(screen, font, "Appuyez sur ESPACE pour le Test", 150, ORANGE)

        elif global_state == "FINISHED":
            ui_buttons = draw_interactive_results(screen, title_font, font, small_font, stats, mouse_pos)

        elif global_state == "EXPERIMENT":
            draw_grid(screen, positions)
            draw_dots(screen, positions, trial_state, is_lit, current_step, current_sequence, target_index)
            
            label = "REPLAY" if replay_mode else ("ENTRAINEMENT" if current_rule_name in sequences.TRAINING_RULES else "TEST")
            col_label = ACTIVE_COLOR if replay_mode else (ORANGE if label == "ENTRAINEMENT" else WHITE)
            screen.blit(font.render(label, True, col_label), (20, 20))

            if trial_state == "GUESS":
                msg = title_font.render("LA SUITE ?", True, ACTIVE_COLOR)
                screen.blit(msg, (SCREEN_WIDTH//2 - 100, 50))
            elif trial_state == "RESULT":
                msg = title_font.render(user_feedback, True, feedback_col)
                screen.blit(msg, (SCREEN_WIDTH//2 - 100, 50))

        pygame.display.flip()

    pygame.quit()

def draw_text_centered(screen, font, text, y_offset, color):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset))
    screen.blit(surf, rect)

def draw_grid(screen, positions):
    start_x, start_y = positions[0]
    end_x, end_y = positions[24]
    for i in range(5):
        x = positions[i][0]
        pygame.draw.line(screen, GRID_LINE_COLOR, (x, start_y), (x, end_y), 2)
        y = positions[i*5][1]
        pygame.draw.line(screen, GRID_LINE_COLOR, (start_x, y), (end_x, y), 2)

def draw_dots(screen, positions, state, is_lit, step, sequence, target):
    for i, pos in enumerate(positions):
        color = CIRCLE_COLOR
        radius = CIRCLE_SIZE
        
        if state == "WATCH" and is_lit and step < len(sequence) - 1:
            if i == sequence[step]:
                color = ACTIVE_COLOR
                radius += 5
                pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), radius)

        elif state == "RESULT":
            if i == target:
                color = SUCCESS_COLOR
                radius += 5
                pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), radius)
        
        is_special = False
        if state == "WATCH" and is_lit and step < len(sequence) - 1 and i == sequence[step]: is_special = True
        if state == "RESULT" and i == target: is_special = True
        
        if not is_special:
             pygame.draw.circle(screen, CIRCLE_COLOR, (int(pos[0]), int(pos[1])), CIRCLE_SIZE)

def draw_interactive_results(screen, title_font, font, small_font, stats, mouse_pos):
    buttons = []
    
    head = title_font.render("BILAN DE LA SESSION", True, WHITE)
    screen.blit(head, (SCREEN_WIDTH//2 - 200, 30))
    
    y = 100
    screen.blit(font.render("Règle", True, WHITE), (50, y))
    screen.blit(font.render("Réussite", True, WHITE), (450, y))
    screen.blit(font.render("Action", True, WHITE), (650, y))
    y += 50
    
    for rule in sequences.TEST_RULES:
        s = stats[rule]
        is_correct = False
        res_txt = "-"
        c = TEXT_COLOR
        
        if s[0] > 0: 
            is_correct = s[1] > 0
            res_txt = "REUSSI" if is_correct else "RATE"
            c = SUCCESS_COLOR if is_correct else ERROR_COLOR
        
        screen.blit(font.render(rule, True, (200, 200, 200)), (50, y))
        screen.blit(font.render(res_txt, True, c), (450, y))
        
        btn_rect = pygame.Rect(640, y, 120, 30)
        is_hover = btn_rect.collidepoint(mouse_pos)
        col_btn = BUTTON_HOVER if is_hover else BUTTON_COLOR
        
        pygame.draw.rect(screen, col_btn, btn_rect, border_radius=5)
        btn_txt = small_font.render("Test", True, WHITE)
        txt_rect = btn_txt.get_rect(center=btn_rect.center)
        screen.blit(btn_txt, txt_rect)
        buttons.append((btn_rect, "REPLAY_RULE", rule))
        
        y += 50
    
    y_bottom = 800
    
    restart_rect = pygame.Rect(SCREEN_WIDTH//2 - 220, y_bottom, 200, 50)
    is_hover_r = restart_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, ACTIVE_COLOR if is_hover_r else (0, 150, 150), restart_rect, border_radius=10)
    r_txt = font.render("Recommencer", True, BG_COLOR)
    screen.blit(r_txt, r_txt.get_rect(center=restart_rect.center))
    buttons.append((restart_rect, "RESTART_ALL", None))
    
    quit_rect = pygame.Rect(SCREEN_WIDTH//2 + 20, y_bottom, 200, 50)
    is_hover_q = quit_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, ERROR_COLOR if is_hover_q else (150, 0, 0), quit_rect, border_radius=10)
    q_txt = font.render("Quitter", True, WHITE)
    screen.blit(q_txt, q_txt.get_rect(center=quit_rect.center))
    buttons.append((quit_rect, "QUIT", None))
    
    return buttons

if __name__ == "__main__":
    run_experiment()