from random import randint
player_hand = [0]
for i in range(0, 10):
    print("\n\nRound " + str(i + 1) + ", You are currently " + ("losing by " + str(abs(player_hand[0])) + " games" if player_hand[0] < 0 else "tied" if player_hand[0] == 0 else "winning by " + str(abs(player_hand[0])) + " games"))
    ai_hand = [min(randint(0, 10) + 2, 10), min(randint(0, 10) + 2, 10)]
    player_hand = player_hand[:1] + [min(randint(0, 10) + 2, 10), min(randint(0, 10) + 2, 10)]
    while sum(player_hand[1:]) < 21 and player_hand[-1] != 0 or sum(ai_hand) < 21 and ai_hand[-1] != 0:
        print(player_hand[1:])
        player_hand.append(min(randint(0, 10) + 2, 10) if bool(input("Type anything to hit, just hit enter to stand: ")) else 0)
        ai_hand.append(0 if sum(ai_hand) >= 16 else min(randint(0, 10) + 2, 10))
    player_hand[0] += 1 if ((sum(player_hand[1:]) > sum(ai_hand) or sum(player_hand[1:]) == 21) and sum(player_hand[1:]) <= 21 and sum(ai_hand) != 21) else -1
print("You " + ("lost by " + str(abs(player_hand[0])) + " games" if player_hand[0] < 0 else "tied" if player_hand[0] == 0 else "won by " + str(abs(player_hand[0])) + " games"))
