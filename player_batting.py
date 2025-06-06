import time
import cv2
from game_logic import play_round
from hand_tracker import detect_hand_and_count_fingers

def player_batting_loop(cap, ai, target=None):
    score = 0
    last_round_time = 0
    round_interval = 2.0
    ai_move_display_time = 1.0
    ai_guess = None
    last_result = None
    game_over_time = None
    game_over = False

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame, player_move = detect_hand_and_count_fingers(frame)

        cv2.putText(frame, "You're batting right now!", (frame.shape[1] - cv2.getTextSize("You're batting right now!", cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)[0][0] - 20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 255, 100), 2)

        now = time.time()
        time_since_last_round = now - last_round_time
        time_remaining = round_interval - time_since_last_round

        if player_move is not None and time_since_last_round >= round_interval:
            ai_guess = ai.get_player_out()
            last_result, points = play_round(player_move, ai_guess)
            ai.update(player_move)
            last_round_time = now

            if last_result == "OUT":
                break
            else:
                score += points

        if ai_guess is not None and time_since_last_round <= ai_move_display_time:
            cv2.putText(frame, f"AI: {ai_guess}", (200, 200),
                        cv2.FONT_HERSHEY_DUPLEX, 4, (0, 255, 255), 6)

        if time_remaining > 0:
            cv2.putText(frame, f"Next round in: {time_remaining:.1f}s", (10, 420),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)

        cv2.putText(frame, f"Score: {score}", (10, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 2)

        cv2.imshow("Odd-Even AI", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if target is not None and score > target:
            break

    return score, last_result