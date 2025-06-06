import cv2
import time
import random

from markov_chain import MarkovChainAI
from player_batting import player_batting_loop
from ai_batting import ai_batting_loop
from hand_tracker import detect_hand_and_count_fingers

# Initialize webcam
cap = cv2.VideoCapture(1)

# Initialize AI
ai = MarkovChainAI()

# Game state variables
game_phase = "toss"
player_choice = None  # "odd" or "even"
player_role = None    # "bat" or "bowl"
ai_role = None
last_round_time = 0.0
round_interval = 2.0
toss_result_time = None
result_parity = None

# Helper: draw centered text
def draw_center_text(frame, text, y_offset=0, scale=2.0, color=(255, 255, 255), thickness=2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    (w, h), _ = cv2.getTextSize(text, font, scale, thickness)
    x = (frame.shape[1] - w) // 2
    y = (frame.shape[0] // 2) + y_offset
    cv2.putText(frame, text, (x, y), font, scale, color, thickness, cv2.LINE_AA)

# Main game loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    now = time.time()
    time_since_last_round = now - last_round_time
    key = cv2.waitKey(1) & 0xFF

    # Toss phase
    if game_phase == "toss":
        if player_choice is None:
            draw_center_text(frame, "TOSS: Press 'o' for Odd or 'e' for Even", -30, 0.9, (200, 200, 255))
            if key == ord('o'):
                player_choice = "odd"
            elif key == ord('e'):
                player_choice = "even"

        elif time_since_last_round >= round_interval:

            player_move = None
            while player_move is None:
                ret, frame = cap.read()
                if not ret:
                    break

                draw_center_text(frame, "Please show a number between 1 and 5", -30, 0.9, (255, 255, 255))
                frame, player_move = detect_hand_and_count_fingers(frame)

                cv2.imshow("Odd-Even AI", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

            if player_move is not None:
                ai_move = random.randint(1, 5)
                toss_sum = player_move + ai_move
                result_parity = "even" if toss_sum % 2 == 0 else "odd"
                player_wins_toss = (player_choice == result_parity)

                toss_result_time = now
                last_round_time = now

                if player_wins_toss:
                    game_phase = "toss_win"
                else:
                    player_role = random.choice(["bat", "bowl"])
                    ai_role = "bowl" if player_role == "bat" else "bat"
                    game_phase = "ready"

                # 3-second result display with toss moves
                start_time = time.time()
                while time.time() - start_time < 3:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    draw_center_text(frame, f"You showed: {player_move} | AI showed: {ai_move}", -90, 0.9, (0, 255, 255))
                    draw_center_text(frame, f"Toss: {'You' if player_wins_toss else 'AI'} won! ({toss_sum} is {result_parity})", -30, 0.9, (100, 255, 255))
                    cv2.imshow("Odd-Even AI", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

    elif game_phase == "toss_win":
        draw_center_text(frame, "You won the toss!", -30, 0.9, (100, 255, 100))
        draw_center_text(frame, "Press 'b' to Bat or 'l' to Bowl", 20, 0.8, (100, 255, 100))
        if key == ord('b'):
            player_role = "bat"
            ai_role = "bowl"
            game_phase = "ready"
        elif key == ord('l'):
            player_role = "bowl"
            ai_role = "bat"
            game_phase = "ready"

    elif game_phase == "ready":
        break  # Exit main loop and begin innings

    cv2.imshow("Odd-Even AI", frame)

    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()

# Inning simulation
if player_role == "bat":
    player_score, _ = player_batting_loop(cap, ai)

    # Show transition screen
    end_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        draw_center_text(frame, "You got OUT! AI will start batting in 3 seconds", 0, 1.0, (0, 0, 255))
        cv2.imshow("Odd-Even AI", frame)
        if time.time() - end_time > 3:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ai_score, _ = ai_batting_loop(cap, ai, target=player_score)
else:
    ai_score, _ = ai_batting_loop(cap, ai)

    # Show transition screen
    end_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        draw_center_text(frame, "You got the AI OUT! Your batting starts in 3 seconds", 0, 1.0, (0, 0, 255))
        cv2.imshow("Odd-Even AI", frame)
        if time.time() - end_time > 3:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    player_score, _ = player_batting_loop(cap, ai, target=ai_score)

# Result screen
result = "You Win!" if player_score > ai_score else "AI Wins!" if ai_score > player_score else "It's a Tie!"
end_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    draw_center_text(frame, "GAME OVER", -40, 2.0, (0, 0, 255))
    draw_center_text(frame, f"You: {player_score}   AI: {ai_score}", 20, 1.0, (255, 255, 0))
    draw_center_text(frame, result, 70, 1.2, (0, 255, 255))

    cv2.imshow("Odd-Even AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or (time.time() - end_time) > 6:
        break

cap.release()
cv2.destroyAllWindows()
